/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["cursos-main/templates/**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily:{
        opens: ['Open Sans', 'serif'],
      },
      colors:{
        pagina:'#E1E3ED',
        card:'#CED6FA',
        input:'#E1E3ED',
        adc:' #03377D',
        linhaForm:'#6E7EC4',
        linhaDiv:'#8590bd',
        linhaFora: '#ADB9EB',
        bg_input:'#e1e3ed',
        coresLinhas:"#cfcbcb",
        fundoTabela:"#ced6fa"
      }
    },
  },
  plugins: [],
}

