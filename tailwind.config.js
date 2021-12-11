const colors = require("tailwindcss/colors");

module.exports = {
    mode: "jit",
    purge: [
        "./src/**/*.html",
        "./src/**/*.njk",
        "./src/**/*.md",
        "./src/**/*.11ty.js",
    ],
    theme: {
        fontFamily: {
            sans: ["Montserrat", "Open Sans", "sans-serif"],
            serif: ["exocet", "Merriweather", "serif"],
        },
        extend: {
            colors: {
                "diablo-dark": "#1c1d21",
                "diablo-darker": "#17181c",
                "diablo-darkest": "#0c0c0e",
                "diablo-light": "#f3f4f6",
                "diablo-yellow": "#B79A64",
            },
        },
        boxShadow: {
            "diablo-input": "0 0 0 4px rgba(183,154,100,0.3)"
        }
    },
    darkMode: "class",
};
