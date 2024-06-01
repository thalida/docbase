module.exports = {
  content: ["./**/*.{html,py,js}"],
  safelist: [
    {
      pattern: /justify-+/,
    },
    {
      pattern: /max-+/,
    },
  ],
};
