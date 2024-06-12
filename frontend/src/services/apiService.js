export const register = async (url, options) => {
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      throw new Error("Error loading api data");
    }
    const data = await response.json();
    return data.username;
  } catch (error) {
    console.error("Error: ", error);
  }
};

export const sendBets = async (url, options) => {
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    console.log("Bets sent successfully: ", data)
    return data
  } catch (error) {
    console.error("Error sending bets: ", error);
  }
}