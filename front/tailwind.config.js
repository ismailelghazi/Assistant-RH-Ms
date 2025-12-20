/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                brand: {
                    dark: '#213448',   // rgb(33, 52, 72)
                    primary: '#547792', // rgb(84, 119, 146)
                    light: '#94B4C1',   // rgb(148, 180, 193)
                    beige: '#EAE0CF',   // rgb(234, 224, 207)
                }
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
