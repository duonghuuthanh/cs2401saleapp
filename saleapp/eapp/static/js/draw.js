function drawChart(data, labels, title, cxtId='myChart', type='pie') {
    const ctx = document.getElementById(cxtId);

    colors = []
    for (let i = 0; i < data.length; i++)
        colors.push(`rgb(${parseInt(Math.random()*255)}, ${parseInt(Math.random()*255)}, ${parseInt(Math.random()*255)})`)

    new Chart(ctx, {
      type: type,
      data: {
        labels: labels,
        datasets: [{
          label: title,
          data: data,
          borderWidth: 1,
          backgroundColor: colors
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
}