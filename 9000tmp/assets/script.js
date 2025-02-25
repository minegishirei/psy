
// https://colorhunt.co/palette/2414689f0d7fea1179f79bd3

// https://colorhunt.co/palette/fff5e0ff6969c70039141e46
var my_palette = {
    "result": '#141E46',
    "condition": '#C70039',
    "hertfull": '#FF6969',
    "else": '#FFF5E0',
}
// #6ACDC2 purple
// #D1C075 yellow 
// #1C3C54 blue
// #7E2A41 red


function insertBR(sentense){
    if(sentense && sentense.length > 20){
        return sentense.match(/.{20}/g).join("<br>");
    }else{
        return ""
    }
}



function applyChartJS(points) {
    points = points.map((row) => {
        return {
            ...row,
            attributes: {
                ...row,
                role: row.description,
                ...{"example" : row.example ? row.example : insertBR(row.description)},
                ...{"explain" : row.explain ? row.explain : insertBR(row.description)}
            },
            events: {
                click: function (e) {
                    window.open(row.link)
                }
            },
            states_hover: {
                cursor: "pointer"
            },
            ...{ color: row.kind ? my_palette[row.kind] : my_palette.else },
            ...{"example" : row.example ? row.example : insertBR(row.description)},
            ...{"explain" : row.explain ? row.explain : insertBR(row.description)}
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
                tooltip: '<div class="tooltipBox" style="background-color: white;">%example</div>',
                label: {
                    text: `
                        <b>%id</b><br>
                        <img width=48 height=48 margin_bottom=4 src=%image><br>
                        <b>%name</b><br>
                        %explain
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