import { mkdir } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { chromium } from "playwright";

const baseUrlFromArg = process.argv.find((arg) => arg.startsWith("--base-url="))?.split("=")[1];
const apiUrlFromArg = process.argv.find((arg) => arg.startsWith("--api-url="))?.split("=")[1];
const BASE_URL = baseUrlFromArg || process.env.SCREENSHOT_BASE_URL || "http://127.0.0.1:8000";
const API_URL = apiUrlFromArg || process.env.SCREENSHOT_API_URL || "http://127.0.0.1:8080";
const SHOTS_DIR = path.resolve(process.cwd(), "../docs/screenshots");

const authenticatedRoutes = [
  { name: "home", path: "/", waitFor: ".roulette-border", capture: "main.app-main > *:first-child" },
  { name: "bets", path: "/bets", waitFor: ".bet-grid, .text-muted", capture: "main.app-main > *:first-child" },
  { name: "about", path: "/about", waitFor: ".about-grid", capture: "main.app-main > *:first-child" },
  { name: "faq", path: "/faq", waitFor: ".payout-table", capture: "main.app-main > *:first-child" },
];

const publicRoutes = [
  { name: "login", path: "/login", waitFor: ".auth-form", capture: "main.app-main > *:first-child" },
  { name: "register", path: "/register", waitFor: ".auth-form", capture: "main.app-main > *:first-child" },
];

async function waitForPageReady(page, selector) {
  await page.waitForLoadState("networkidle");
  await page.waitForSelector(selector, { timeout: 15000 });
  await page.waitForTimeout(800);
}

async function loginFlow(context, page) {
  const suffix = Date.now();
  const username = `shot_user_${suffix}`;
  const password = "shot_pass_123";

  const registerResponse = await page.request.post(`${API_URL}/api/create/`, {
    data: {
      username,
      password,
    },
  });
  if (!registerResponse.ok()) {
    throw new Error(`User register failed with status ${registerResponse.status()}`);
  }

  const loginResponse = await page.request.post(`${API_URL}/api/token/`, {
    data: {
      username,
      password,
    },
  });
  if (!loginResponse.ok()) {
    throw new Error(`Login failed with status ${loginResponse.status()}`);
  }

  const loginPayload = await loginResponse.json();
  const accessToken = loginPayload?.data?.access;
  const refreshToken = loginPayload?.data?.refresh;
  if (!accessToken || !refreshToken) {
    throw new Error("Token payload is missing.");
  }

  const apiHost = new URL(API_URL).hostname;
  await context.addCookies([
    {
      name: "access_token",
      value: accessToken,
      domain: apiHost,
      path: "/",
      httpOnly: true,
      secure: false,
      sameSite: "Lax",
    },
    {
      name: "refresh_token",
      value: refreshToken,
      domain: apiHost,
      path: "/",
      httpOnly: true,
      secure: false,
      sameSite: "Lax",
    },
  ]);

  await page.goto(`${BASE_URL}/`, { waitUntil: "domcontentloaded" });
  await waitForPageReady(page, ".roulette-border");

  const depositButton = page.locator("button", { hasText: "+500" });
  if (await depositButton.count()) {
    await depositButton.first().click();
    await page.waitForTimeout(1200);
  }
}

async function captureRoute(page, route) {
  await page.goto(`${BASE_URL}${route.path}`, { waitUntil: "domcontentloaded" });
  await waitForPageReady(page, route.waitFor);
  const screenshotPath = path.join(SHOTS_DIR, `${route.name}.png`);

  const appShell = page.locator("#app.app-shell").first();
  if (await appShell.count()) {
    const shellBounds = await appShell.boundingBox();
    if (shellBounds) {
      const pageSize = await page.evaluate(() => ({
        width: document.documentElement.scrollWidth,
        height: document.documentElement.scrollHeight,
      }));
      const margin = 20;
      const x = Math.max(0, shellBounds.x - margin);
      const y = Math.max(0, shellBounds.y - margin);
      const width = Math.min(pageSize.width - x, shellBounds.width + margin * 2);
      const height = Math.min(pageSize.height - y, shellBounds.height + margin * 2);

      await page.screenshot({
        path: screenshotPath,
        clip: { x, y, width, height },
      });
      return;
    }
  }

  const content = page.locator(route.capture || "main.app-main > *:first-child").first();
  if (await content.count()) {
    await content.screenshot({ path: screenshotPath });
    return;
  }

  await page.screenshot({ path: screenshotPath, fullPage: true });
}

async function main() {
  await mkdir(SHOTS_DIR, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1600, height: 1200 } });
  const page = await context.newPage();

  await loginFlow(context, page);

  for (const route of authenticatedRoutes) {
    await captureRoute(page, route);
  }

  await context.clearCookies();

  for (const route of publicRoutes) {
    await captureRoute(page, route);
  }

  await context.close();
  await browser.close();
  console.log(`Screenshots saved to: ${SHOTS_DIR}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
