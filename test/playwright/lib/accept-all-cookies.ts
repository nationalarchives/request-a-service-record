import { test } from "@playwright/test";
import { cookiePreferencesSetKey } from "../../../playwright.config.ts";

const acceptAllCookies = () => {
  test.beforeEach(async ({ context, baseURL }) => {
    await context.addCookies([
      {
        name: cookiePreferencesSetKey,
        value: "true",
        domain: baseURL,
        path: "/",
      },
    ]);
    await context.addCookies([
      {
        name: "cookies_policy",
        value:
          "%7B%22usage%22%3Atrue%2C%22settings%22%3Atrue%2C%22marketing%22%3Atrue%2C%22essential%22%3Atrue%7D",
        domain: baseURL,
        path: "/",
      },
    ]);
  });
};

export default acceptAllCookies;
