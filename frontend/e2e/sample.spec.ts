import { test, expect } from '@playwright/test';
test('loads chat', async ({ page }) =>{ await page.goto('/chat'); await expect(page.locator('text=Chat')).toBeVisible(); });
