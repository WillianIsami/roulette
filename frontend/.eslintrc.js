module.exports = {
  env: {
    node: true,
  },
  extends: ["eslint:recommended", "plugin:vue/vue3-essential", "prettier"],
  parserOptions: {
    parser: "babel-eslint",
  },
  rules: {
    'no-unused-vars': ['error', { 'argsIgnorePattern': '^_' }],
    "vue/no-unused-components": "warn",
    "vue/no-unused-vars": "warn",
    "vue/require-prop-types": "warn",
    "vue/require-default-prop": "warn",
  },
};
