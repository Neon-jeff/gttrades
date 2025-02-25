/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ["./templates/**/*.html", "./static/js/*.js"],
  theme: {
    extend: {
      keyframes: {
        sliding: {
          "0%": {
            transform: "translate(500px,0)",
          },
          "70%": {
            transform: "translate(0,0)",
            transform: "scale(1.3)",
          },
          "100%": {
            transform: "scale(1)",
          },
        },
        headHeroText: {
          "0%": {
            transform: "translate(-500px,0)",
            opacity: 0,
          },
          "100%": {
            transform: "translate(0,0)",
            opacity: 1,
          },
        },
        heroParagraph: {
          "0%": {
            transform: "translate(0,50px)",
            opacity: 0,
          },
          "40%": {
            opacity: 0.5,
          },
          "100%": {
            transform: "translate(0,0)",
            opacity: 1,
          },
        },
      },
      animation: {
        slide: "sliding 1s ease-in ",
        herotext: "headHeroText 1s ease-in",
        heroparagraph: "heroParagraph 1s ease-in",
      },
      colors: {
        pri: "#212529",
        secondary: "#343a40",
        main: "#bddb39",
        sub: "#0f151c",
        light: "#83d2c0",
        dark:"#000000"
      },
      fontFamily: {
        workSans: ["Work Sans", "sans-serif"],
        lato: ["Lato", "sans-serif"],
      },
    },
    screens: {
      xs: "480px",
      ss: "620px",
      sm: "768px",
      md: "1060px",
      lg: "1200px",
      xl: "1700px",
      xss: "360px",
    },
  },
  plugins: [],
};
