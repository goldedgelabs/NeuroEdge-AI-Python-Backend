import { test, expect } from '@playwright/test';
test('streaming token flow', async ({ page }) => {
  await page.goto('/chat');
  await page.fill('[data-testid="chat-input"]', 'hello stream');
  await page.click('[data-testid="send-btn"]');
  // wait for at least 3 tokens to appear
  await page.waitForSelector('[data-testid="assistant-message-stream"]');
  const tokens = await page.$$('[data-testid="assistant-message-stream"]');
  expect(tokens.length).toBeGreaterThan(0);
});
