import { extendTheme } from "@chakra-ui/react";

const theme = extendTheme({
  fonts: {
      heading: 'var(--font-rubik)',
      body: 'var(--font-rubik)',
    },
    colors: {
      primary: {
        50: "#ebf8ff",  // Lightest Blue
        100: "#ceedff",
        200: "#addbff",
        300: "#8cc9ff",
        400: "#6bb7ff",
        500: "#4AA5FF",  // Original primary color (Vivid Blue)
        600: "#3989e5",
        700: "#296dcc",
        800: "#1951b3",
        900: "#093599",  // Darkest Blue
      },
      accent: {
        50: "#fff9e6",  // Lightest Yellow
        100: "#ffefcc",
        200: "#ffe5b3",
        300: "#ffdb99",
        400: "#ffd180",
        500: "#FFC966",  // Original accent color (Bright Yellow)
        600: "#e5b24d",
        700: "#cc9e34",
        800: "#b38a1b",
        900: "#997602",  // Darkest Yellow
      },
  },
  
});

export default theme;
