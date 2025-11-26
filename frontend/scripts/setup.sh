#!/usr/bin/env bash
cp .env.example .env.local
npm ci
npm run build
