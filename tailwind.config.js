module.exports = {
  daisyui: {
    themes: ["light", "dark"],
  },
  darkMode: ["class", '[data-theme="dark"]'],
  content: [
    './apps/**/*.html',
    './assets/**/*.js',
    './assets/**/*.ts',
    './templates/**/*.html',
    './apps/web/templatetags/form_tags.py',
  ],
  safelist: [
    'alert-success',
    'alert-info',
    'alert-error',
    'alert-warning',
    'pg-bg-danger',
    'pg-bg-success',
  ],
  theme: {
    extend: {
      aspectRatio: {
        '3/2': '3 / 2',
      },
    },
    container: {
      center: true,
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
    require("daisyui"),
  ],
}
