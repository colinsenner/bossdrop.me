const colors = require("tailwindcss/colors");

module.exports = {
    mode: "jit",
    purge: [
        "./src/**/*.html",
        "./src/**/*.njk",
        "./src/**/*.md",
        "./src/**/*.11ty.js",
        "./src/**/*.js",
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
                "diablo-light": "#e5e7eb",
                "diablo-yellow": "#b79a64",
                "diablo-yellow-darker": "#9d7f48",
                "diablo-red": "#ff4747",
                "diablo-red-darker": "#cc0000",
            },
        },
        boxShadow: {
            "diablo-input": "0 0 0 4px rgba(183,154,100,0.3)"
        }
    },
    darkMode: "class",
};
