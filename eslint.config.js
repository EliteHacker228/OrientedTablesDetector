import { Linter } from "eslint";

/** @type {Linter.Config} */
const config = {
  files: ["**/*.ts"],
  languageOptions: {
    parser: "@typescript-eslint/parser",
    parserOptions: {
      project: "./front/tsconfig.json",
    },
  },
  plugins: {
    "@typescript-eslint": require("@typescript-eslint/eslint-plugin"),
    "@angular-eslint": require("@angular-eslint/eslint-plugin"),
  },
  rules: {},
  settings: {},
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@angular-eslint/recommended",
  ],
  env: {
    browser: true,
    node: true,
    es2021: true,
  },
};

export default config;
