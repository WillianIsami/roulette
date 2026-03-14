<template>
  <section class="glass-card p-4 p-md-5">
    <h1 class="page-title">{{ $t("aboutPage.title") }}</h1>
    <p class="page-lead mb-4">{{ $t("aboutPage.lead") }}</p>

    <div class="about-grid">
      <article class="about-item">
        <h3>{{ $t("aboutPage.backendTitle") }}</h3>
        <p>{{ $t("aboutPage.backendDescription") }}</p>
      </article>
      <article class="about-item">
        <h3>{{ $t("aboutPage.uxTitle") }}</h3>
        <p>{{ $t("aboutPage.uxDescription") }}</p>
      </article>
      <article class="about-item">
        <h3>{{ $t("aboutPage.qualityTitle") }}</h3>
        <p>{{ $t("aboutPage.qualityDescription") }}</p>
      </article>
    </div>
  </section>
</template>

<script>
export default {
  name: "AboutView",
};
</script>

<style scoped>
.about-grid {
  display: grid;
  gap: 0.8rem;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.about-item {
  border: 1px solid #e1d5b8;
  border-radius: 14px;
  padding: 0.9rem;
  background: #fffdf8;
}

.about-item h3 {
  font-family: "Racing Sans One", sans-serif;
  color: #214a34;
  margin-bottom: 0.4rem;
  font-size: 1.15rem;
}

.about-item p {
  margin: 0;
  color: #3a5448;
}
</style>
