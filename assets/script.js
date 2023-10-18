
var my_palette = {
    "result": '#1C3C54',
    "condition": '#D1C075',
    "hertfull": '#CD6AB9',
    "else": 'white',
}
// #6ACDC2 purple
// #D1C075 yellow 
// #1C3C54 blue
// #7E2A41 red



function applyChartJS(points) {
    points = points.map((row) => {
        return {
            ...row,
            attributes: {
                ...row,
                role: row.description
            },
            events: {
                click: function (e) {
                    window.open(row.link)
                }
            },
            states_hover: {
                cursor: "pointer"
            },
            ...{ color: row.kind ? my_palette[row.kind] : my_palette.else }
        }
    })

    var chart = JSC.chart('chartDiv', {
        debug: true,
        type: 'organizational down',
        defaultAnnotation: {
            padding: [5, 10],
            margin: [50, 0],
            radius: 15
        },
        defaultTooltip: {
            asHTML: true,
            outline: 'none',
            zIndex: 10
        },
        annotation: {
            padding: 9,
            corners: ['cut', 'square', 'cut', 'square'],
            margin: [15, 5, 10, 0]
        },
        defaultSeries: {
            color: 'white',
            defaultPoint: {
                outline_width: 0,
                connectorLine: { radius: 140, width: 2 },
                tooltip: '<div class="tooltipBox">%example</div>',
                label: {
                    text: `
                        <b>%id</b><br>
                        <img width=48 height=48 margin_bottom=4 src=%image><br>
                        <b>%name</b><br>
                        <br><span style="font-size:10px; ">%description</span><br>
                        `,
                    maxWidth: 500,
                    autoWrap: false
                }
            }
        },

        series: [{ points: points }]
    });
}
function onClickNode(link) {
    window.location.href = link
}