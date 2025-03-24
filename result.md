<!DOCTYPE html>
<html lang="en">

<body>
  <script src="https://cdn.jsdelivr.net/npm/gojs@3.0.19/release/go.js"></script>
  <div id="allSampleContent" class="p-4 w-full">
    <script src="https://cdn.jsdelivr.net/npm/create-gojs-kit@3.0.19/dist/extensions/Figures.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/create-gojs-kit@3.0.19/dist/extensions/Themes.js"></script>
    <script id="code">
      isSample = true
      isExplainOpen = false
      function init() {
        myDiagram = new go.Diagram('myDiagramDiv', {
          allowCopy: false,
          'draggingTool.dragsTree': true,
          'commandHandler.deletesTree': true,
          layout: new go.TreeLayout({ angle: 90, arrangement: go.TreeArrangement.FixedRoots }),
          'undoManager.isEnabled': true,
          // use "Modern" themes from extensions/Themes
          'themeManager.themeMap': new go.Map([
            { key: 'light', value: Modern },
            { key: 'dark', value: ModernDark }
          ]),
          'themeManager.changesDivBackground': true,
          'themeManager.currentTheme': document.getElementById('theme').value
        });

        myDiagram.themeManager.set('', {
          colors: {
            primary: '#155e75',
            terminal: '#047857'
          }
        });

        // when the document is modified, add a "*" to the title and enable the "Save" button
        myDiagram.addDiagramListener('Modified', (e) => {
          var button = document.getElementById('SaveButton');
          if (button) button.disabled = !myDiagram.isModified;
          var idx = document.title.indexOf('*');
          if (myDiagram.isModified) {
            if (idx < 0) document.title += '*';
          } else {
            if (idx >= 0) document.title = document.title.slice(0, idx);
          }
        });

        go.Shape.defineFigureGenerator('Van', function (shape, w, h) {
          var geo = go.Geometry.parse(
            'M37.409,18.905l-4.946-7.924c-0.548-0.878-1.51-1.411-2.545-1.411H3c-1.657,0-3,1.343-3,3v16.86c0,1.657,1.343,3,3,3h0.787 c0.758,1.618,2.391,2.75,4.293,2.75s3.534-1.132,4.292-2.75h20.007c0.758,1.618,2.391,2.75,4.293,2.75 c1.9,0,3.534-1.132,4.291-2.75h0.787c1.656,0,3-1.343,3-3v-2.496C44.75,22.737,41.516,19.272,37.409,18.905z M8.087,32.395 c-1.084,0-1.963-0.879-1.963-1.963s0.879-1.964,1.963-1.964s1.963,0.88,1.963,1.964S9.171,32.395,8.087,32.395z M26.042,21.001 V15.57v-2.999h3.876l5.264,8.43H26.042z M36.671,32.395c-1.084,0-1.963-0.879-1.963-1.963s0.879-1.964,1.963-1.964 s1.963,0.88,1.963,1.964S37.755,32.395,36.671,32.395z'
          );
          return geo.scale(w / geo.bounds.width, h / geo.bounds.height);
        });
        go.Shape.defineFigureGenerator('SUV', function (shape, w, h) {
          var geo = go.Geometry.parse(
            'M246,90.011V59.995c0-5.523-4.48-9.995-10-9.995h-50L156.97,6.416C155.11,3.634,152.34,2,149,2H28 c-5.52,0-10,4.446-10,9.969V30h-8c-4.42,0-8,3.56-8,7.983v40.022C2,82.427,5.58,86,10,86h8v20h16.458 c2.8-15.959,16.702-28.066,33.462-28.066c16.75,0,30.708,12.107,33.518,28.066h72.958c2.8-15.959,16.764-28.066,33.524-28.066 c16.75,0,30.624,12.107,33.434,28.066H250c4.42,0,8-3.563,8-7.985v-8.004H246z M86,50H30V13.97h56V50z M98,50V13.97h48L170,50H98z M68,138c-14.336,0-26.083-11.706-26.083-26.051s11.664-26.014,26-26.014s26,11.669,26,26.014S82.336,138,68,138z M67.917,99.943 c-6.617,0-12,5.386-12,12.006c0,6.621,5.383,12.006,12,12.006s12-5.386,12-12.006C79.917,105.329,74.534,99.943,67.917,99.943z M208,138c-14.337,0-26.083-11.706-26.083-26.051s11.663-26.014,26-26.014s26,11.669,26,26.014S222.337,138,208,138z M207.917,99.943c-6.617,0-12,5.386-12,12.006c0,6.621,5.383,12.006,12,12.006s12-5.386,12-12.006 C219.917,105.329,214.534,99.943,207.917,99.943z'
          );
          return geo.scale(w / geo.bounds.width, h / geo.bounds.height);
        });
        go.Shape.defineFigureGenerator('Hammer', function (shape, w, h) {
          var geo = go.Geometry.parse(
            'M19 5.5a4.5 4.5 0 01-4.791 4.49c-.873-.055-1.808.128-2.368.8l-6.024 7.23a2.724 2.724 0 11-3.837-3.837L9.21 8.16c.672-.56.855-1.495.8-2.368a4.5 4.5 0 015.873-4.575c.324.105.39.51.15.752L13.34 4.66a.455.455 0 00-.11.494 3.01 3.01 0 001.617 1.617c.17.07.363.02.493-.111l2.692-2.692c.241-.241.647-.174.752.15.14.435.216.9.216 1.382zM4 17a1 1 0 100-2 1 1 0 000 2z'
          );
          return geo.scale(w / geo.bounds.width, h / geo.bounds.height);
        });

        // each action is represented by a shape and some text
        var actionTemplate = new go.Panel('TableRow')
          .add(
            new go.Shape({ column: 0, width: 20, height: 20, fill: null }).bind('figure').theme('stroke', 'text'),
            new go.TextBlock({ column: 1 }, { font: '11pt Verdana, sans-serif' }).bind('text').theme('stroke', 'text'),
            new go.TextBlock({ column: 2, font: '11pt Verdana, sans-serif' })
              .bindObject('text', 'itemIndex', (i) => `[${i}]`)
              .theme('stroke', 'text')
          );

        var regularNodeColor = (category) => {
          if (category == 'write') {
            return '#155e75'
          }
          if (category == 'read') {
            return '#7D1C4A'
          }
          if (category == 'persol') {
            return '#493D60'
          }
          return '#155e75'
        }

        // each regular Node has body consisting of a title followed by a collapsible list of actions,
        // controlled by a PanelExpanderButton, with a TreeExpanderButton underneath the body
        myDiagram.nodeTemplate = // the default node template
          new go.Node('Vertical', { selectionObjectName: 'BODY' })
            // the main "BODY" consists of a RoundedRectangle surrounding nested Panels
            .bindTwoWay('isTreeExpanded') // remember the expansion state for
            .bindTwoWay('wasTreeExpanded') //   when the model is re-loaded
            .add(
              new go.Panel('Auto', { name: 'BODY' })
                .add(
                  new go.Shape('RoundedRectangle', { strokeWidth: 0 }).bind('fill', 'method', regularNodeColor),
                  new go.Panel('Vertical', { margin: 3 })
                    .add(
                      // the title
                      new go.TextBlock({
                        stretch: go.Stretch.Horizontal,
                        font: 'bold 12pt Verdana, sans-serif',
                        stroke: 'white'
                      })
                        .bind('text', 'question'),
                      // the optional list of actions
                      new go.Panel('Vertical', {
                        stretch: go.Stretch.Horizontal,
                        visible: false
                      }) // not visible unless there is at least one action
                        .bind('visible', 'actions', (acts) => Array.isArray(acts) && acts.length > 0)
                        .add(
                          // headered by a label and a PanelExpanderButton inside a Table
                          new go.Panel('Table', { stretch: go.Stretch.Horizontal })
                            .add(
                              new go.TextBlock('Example', {
                                alignment: go.Spot.Left,
                                font: '10pt Verdana, sans-serif',
                                stroke: 'white'
                              }),
                              go.GraphObject.build('PanelExpanderButton',
                                {
                                  column: 1,
                                  alignment: go.Spot.Right,
                                  'ButtonIcon.stroke': 'white'
                                },
                                'COLLAPSIBLE' // name of the object to make visible or invisible
                              )
                            ), // end Table panel
                          // with the list data bound in the Table Panel
                          new go.Panel('Table', {
                            name: 'COLLAPSIBLE', // identify to the PanelExpanderButton
                            visible: isExplainOpen, // default close
                            padding: 2,
                            stretch: go.Stretch.Horizontal, // take up whole available width
                            defaultAlignment: go.Spot.Left, // thus no need to specify alignment on each element
                            defaultSeparatorPadding: 3,
                            itemTemplate: actionTemplate // the Panel created for each item in Panel.itemArray
                          })
                            .theme('background', 'div')
                            .bind('itemArray', 'actions')
                          // bind Panel.itemArray to nodedata.actions
                        ) // end optional Vertical Panel
                    ) // end outer Vertical Panel
                ), // end "BODY"  Auto Panel
              new go.Panel( // this is underneath the "BODY"
                { height: 17 }) // always this height, even if the TreeExpanderButton is not visible
                .add(go.GraphObject.build('TreeExpanderButton'))
            );

        // define a second kind of Node:
        myDiagram.nodeTemplateMap.add(
          'Terminal',
          new go.Node('Spot')
            .add(
              new go.Shape('Circle', { width: 55, height: 55, strokeWidth: 0 }).theme('fill', 'terminal'),
              new go.TextBlock({ font: '10pt Verdana, sans-serif', stroke: 'white' }).bind('text')
            )
        );

        myDiagram.linkTemplate = new go.Link(
          { routing: go.Routing.Orthogonal, deletable: false, corner: 10, toShortLength: 4 }
        )
          .add(
            new go.Shape({ strokeWidth: 2 }).theme('stroke', 'link'),
            new go.Shape({ toArrow: 'Standard', strokeWidth: 0 }) // the arrowhead
              .theme('fill', 'link')
          );

        myDiagram.layout = new go.LayeredDigraphLayout({
          direction: 90, // 上から下に配置 (0: 左→右, 90: 上→下)
          layerSpacing: 50, // レイヤー間のスペース
          columnSpacing: 30 // 列間のスペース
        });
        myDiagram.model = go.Model.fromJson(
          `{"copiesArrays": true, "copiesArrayObjects": true, "nodeDataArray": [{"key": 0, "type": "Table", "question": "外交性が低い", "actions": [{"text": "", "figure": "BpmnTaskMessage"}, {"text": "a", "figure": "Caution"}], "example": "a", "effect": "「かかわりを持っている」「他人に注目されている」", "method": "persol", "file_path": "/psy/blog/1000PERSOL/null/main.md"}, {"key": 1, "type": "Table", "question": "開放性が低い", "actions": [{"text": "", "figure": "Caution"}, {"text": "a", "figure": "Hammer"}], "example": "a", "effect": "終了", "method": "persol", "file_path": "/psy/blog/1000PERSOL/null/main.md", "category": "Terminal", "text": "開放性が低い"}, {"key": 2, "type": "Table", "question": "外交性が高い", "actions": [{"text": "", "figure": "Hammer"}, {"text": "a", "figure": "BpmnTaskMessage"}], "example": "a", "effect": "終了", "method": "persol", "file_path": "/psy/blog/1000PERSOL/null/main.md", "category": "Terminal", "text": "外交性が高い"}, {"key": 3, "type": "Table", "question": "神経症傾向の高い人", "actions": [{"text": "", "figure": "Hammer"}, {"text": "a", "figure": "BpmnTaskMessage"}], "example": "a", "effect": "終了", "method": "persol", "file_path": "/psy/blog/1000PERSOL/null/main.md", "category": "Terminal", "text": "神経症傾向の高い人"}, {"key": 4, "type": "Table", "question": "犯罪者", "actions": [{"text": "", "figure": "Hammer"}, {"text": "a", "figure": "Caution"}], "example": "a", "effect": "終了", "method": "persol", "file_path": "/psy/blog/1000PERSOL/null/main.md", "category": "Terminal", "text": "犯罪者"}, {"key": 5, "type": "Table", "question": "ホモ・デリンクエンス", "actions": [{"text": "原始人の遺伝的特徴が隔世遺伝によって再現した原始的（先祖返り）又は退行的な起源を持つ複数の身体的異常の発現", "figure": "BpmnTaskMessage"}, {"text": "犯罪者はこうした退行的隔世遺伝が生じた、人類の下等な段階の甦り、人類の一変種「ホモ・デリンクエンス（犯罪人）」という説", "figure": "Caution"}, {"text": "小さな脳", "figure": "Caution"}, {"text": "厚い頭蓋骨", "figure": "Hammer"}, {"text": "大きな顎、顎の前方への突出", "figure": "BpmnTaskMessage"}, {"text": "低い額", "figure": "Caution"}, {"text": "高い頬骨", "figure": "BpmnTaskMessage"}, {"text": "平らな鼻、または上向きの鼻", "figure": "Caution"}, {"text": "取っ手のような形をした耳", "figure": "BpmnTaskMessage"}, {"text": "鷹のような鼻", "figure": "Caution"}, {"text": "肉付きのよい唇", "figure": "Hammer"}, {"text": "異常な歯並び", "figure": "Caution"}, {"text": "厳しい目つき、泳ぐ目線", "figure": "Caution"}, {"text": "毛深さ", "figure": "Hammer"}, {"text": "ひげが少ない、またはない", "figure": "Hammer"}, {"text": "下肢に比べて腕が長い", "figure": "Hammer"}], "example": "小さな脳,厚い頭蓋骨,大きな顎、顎の前方への突出,低い額,高い頬骨,平らな鼻、または上向きの鼻,取っ手のような形をした耳,鷹のような鼻,肉付きのよい唇,異常な歯並び,厳しい目つき、泳ぐ目線,毛深さ,ひげが少ない、またはない,下肢に比べて腕が長い", "effect": "犯罪者", "method": "persol", "file_path": "/psy/blog/1000PERSOL/1800brain/crime.md"}, {"key": 6, "type": "Table", "question": "オタク文化への興味,顔文字", "actions": [{"text": "まずフェイスブック投稿で相関が見受けられたもの", "figure": "Caution"}, {"text": "インターネット、コンピューター", "figure": "Hammer"}, {"text": "アニメ、マンガ、日本の", "figure": "Caution"}, {"text": "ポケモン、ファイナルファンタジー", "figure": "Caution"}, {"text": "顔文字(>_<)", "figure": "Caution"}], "example": "インターネット、コンピューター,アニメ、マンガ、日本の,ポケモン、ファイナルファンタジー,顔文字(>_<)", "effect": "外交性が低い", "method": "persol", "file_path": "/psy/blog/1000PERSOL/0000bigfive/1000extrovertism.md"}, {"key": 7, "type": "Table", "question": "絵文字の使用", "actions": [{"text": "絵文字を使用する場合は外向性が高いという研究結果も出ている", "figure": "BpmnTaskMessage"}, {"text": "👍", "figure": "Hammer"}], "example": "👍", "effect": "外交性が高い", "method": "persol", "file_path": "/psy/blog/1000PERSOL/0000bigfive/1000extrovertism.md"}, {"key": 8, "type": "Table", "question": "所有権の意識", "actions": [{"text": "Facebook投稿での相関があるテキスト", "figure": "Caution"}, {"text": "「OOしたほうがいい」という肯定的意見よりも「OOしてはいけない」という**ルールで縛る方向性**で意見を出す。", "figure": "BpmnTaskMessage"}, {"text": "あなた", "figure": "Hammer"}, {"text": "あなたの", "figure": "BpmnTaskMessage"}, {"text": "してはいけない", "figure": "Caution"}], "example": "あなた,あなたの,してはいけない", "effect": "開放性が低い", "method": "persol", "file_path": "/psy/blog/1000PERSOL/0000bigfive/2000openness.md"}, {"key": 9, "type": "Table", "question": "ネガティブワード", "actions": [{"text": "", "figure": "BpmnTaskMessage"}, {"text": "fucking", "figure": "Hammer"}, {"text": "fuck", "figure": "Caution"}, {"text": "shit", "figure": "Caution"}, {"text": "crap", "figure": "Caution"}, {"text": "バカ", "figure": "Caution"}, {"text": "がっかりした", "figure": "Hammer"}, {"text": "うんざり", "figure": "Caution"}, {"text": "病む", "figure": "Caution"}, {"text": "イライラする", "figure": "Hammer"}, {"text": "退屈", "figure": "Caution"}, {"text": "ひどい", "figure": "BpmnTaskMessage"}, {"text": "鬱", "figure": "BpmnTaskMessage"}, {"text": "寂しい", "figure": "BpmnTaskMessage"}, {"text": "独り", "figure": "BpmnTaskMessage"}, {"text": "地獄", "figure": "Hammer"}, {"text": "死ぬ", "figure": "Hammer"}, {"text": "嫌い", "figure": "BpmnTaskMessage"}, {"text": "悪夢", "figure": "Caution"}, {"text": "泣いている", "figure": "Hammer"}, {"text": "xd　>_<　x_x", "figure": "Caution"}], "example": "fucking,fuck,shit,crap,バカ,がっかりした,うんざり,病む,イライラする,退屈,ひどい,鬱,寂しい,独り,地獄,死ぬ,嫌い,悪夢,泣いている,xd　>_<　x_x", "effect": "神経症傾向の高い人,犯罪者", "method": "persol", "file_path": "/psy/blog/1000PERSOL/0000bigfive/4000neuroticism.md"}, {"key": 10, "type": "Table", "question": "使用する言語が異なる", "actions": [{"text": "言語相対性仮説", "figure": "Hammer"}, {"text": "母国語となる言語によって語彙や構文法などには偏りがあり、このことが民族的な認知・思考の偏りを支配している", "figure": "BpmnTaskMessage"}, {"text": "母国語が異なる人々が、異なる認知や思考の傾向を持つ", "figure": "BpmnTaskMessage"}], "example": "母国語が異なる人々が、異なる認知や思考の傾向を持つ", "effect": "人の思考や認知の変化", "method": "persol", "file_path": "/psy/blog/1000PERSOL/1900education/child/20250225094658.md"}, {"key": 11, "type": "Table", "question": "マザリーズ", "actions": [{"text": "マザリーズが子供の言葉の発達を促進するように働く。母親を始め、大人が乳幼児に向けた、意識するしないにかかわらず自然と口をついて出る、声の調子が高くゆったりとしたリズムの話し方", "figure": "BpmnTaskMessage"}, {"text": "母親が、乳幼児に向けた話し方が、子供の言葉の発達を促進する", "figure": "Hammer"}], "example": "母親が、乳幼児に向けた話し方が、子供の言葉の発達を促進する", "effect": "言語獲得の促進,傾聴の促進", "method": "persol", "file_path": "/psy/blog/1000PERSOL/1900education/child/mother.md"}, {"key": 12, "type": "Table", "question": "母親との関係における規定不安", "actions": [{"text": "子供時代の母親との関係における基底不安が神経症の要因となる", "figure": "Hammer"}, {"text": "孤独感や無力感を克服するために、子供時代の母親との関係を振り返る", "figure": "BpmnTaskMessage"}], "example": "孤独感や無力感を克服するために、子供時代の母親との関係を振り返る", "effect": "神経症傾向の高い人", "method": "persol", "file_path": "/psy/blog/1000PERSOL/1900education/child/20250225093701.md"}, {"key": 13, "type": "Table", "question": "自主的な行動の誘発", "actions": [{"text": "", "figure": "BpmnTaskMessage"}, {"text": "やる気が満ち溢れている状態", "figure": "Caution"}], "example": "やる気が満ち溢れている状態", "effect": "終了", "method": "write", "file_path": "/psy/blog/5000WRITE/null/main.md", "category": "Terminal", "text": "自主的な行動の誘発"}, {"key": 14, "type": "Table", "question": "同じ行動を取り続ける", "actions": [{"text": "", "figure": "BpmnTaskMessage"}, {"text": "やる気が満ち溢れている状態", "figure": "Caution"}], "example": "やる気が満ち溢れている状態", "effect": "終了", "method": "write", "file_path": "/psy/blog/5000WRITE/null/main.md", "category": "Terminal", "text": "同じ行動を取り続ける"}, {"key": 15, "type": "Table", "question": "ステレオタイプに一致", "actions": [{"text": "", "figure": "Hammer"}, {"text": "「彼は医者だから医療の知識がすごい」", "figure": "Caution"}], "example": "「彼は医者だから医療の知識がすごい」", "effect": "終了", "method": "write", "file_path": "/psy/blog/5000WRITE/null/main.md", "category": "Terminal", "text": "ステレオタイプに一致"}, {"key": 16, "type": "Table", "question": "期待通り", "actions": [{"text": "", "figure": "Hammer"}, {"text": "「思った通り」", "figure": "BpmnTaskMessage"}], "example": "「思った通り」", "effect": "終了", "method": "write", "file_path": "/psy/blog/5000WRITE/null/main.md", "category": "Terminal", "text": "期待通り"}, {"key": 17, "type": "Table", "question": "推論機能の誘発", "actions": [{"text": "", "figure": "Hammer"}, {"text": "a", "figure": "Hammer"}], "example": "a", "effect": "終了", "method": "write", "file_path": "/psy/blog/5000WRITE/null/main.md", "category": "Terminal", "text": "推論機能の誘発"}, {"key": 18, "type": "Table", "question": "あゆみより", "actions": [{"text": "", "figure": "Caution"}, {"text": "a", "figure": "Caution"}], "example": "a", "effect": "終了", "method": "write", "file_path": "/psy/blog/5000WRITE/null/main.md", "category": "Terminal", "text": "あゆみより"}, {"key": 19, "type": "Table", "question": "回避行動", "actions": [{"text": "", "figure": "BpmnTaskMessage"}, {"text": "a", "figure": "BpmnTaskMessage"}], "example": "a", "effect": "終了", "method": "write", "file_path": "/psy/blog/5000WRITE/null/main.md", "category": "Terminal", "text": "回避行動"}, {"key": 20, "type": "Table", "question": "促進行動", "actions": [{"text": "", "figure": "Hammer"}, {"text": "a", "figure": "Caution"}], "example": "a", "effect": "終了", "method": "write", "file_path": "/psy/blog/5000WRITE/null/main.md", "category": "Terminal", "text": "促進行動"}, {"key": 21, "type": "Table", "question": "「かかわりを持っている」「他人に注目されている」", "actions": [{"text": "", "figure": "Hammer"}, {"text": "人から手伝いを頼まれ引き受けると2度目以降も断りにくくなる", "figure": "Caution"}], "example": "人から手伝いを頼まれ引き受けると2度目以降も断りにくくなる", "effect": "一貫性の法則", "method": "write", "file_path": "/psy/blog/5000WRITE/5000write_base/consistency.md"}, {"key": 22, "type": "Table", "question": "一貫性の法則", "actions": [{"text": "", "figure": "BpmnTaskMessage"}, {"text": "好きな歌手のCDだからという理由だけで買ってしまう", "figure": "BpmnTaskMessage"}], "example": "好きな歌手のCDだからという理由だけで買ってしまう", "effect": "同じ行動を取り続ける", "method": "write", "file_path": "/psy/blog/5000WRITE/5000write_base/consistency.md"}, {"key": 23, "type": "Table", "question": "生存率の提示", "actions": [{"text": "", "figure": "Hammer"}, {"text": "癌の外科手術の効果について死亡率の代わりに生存率が示された場合、医師が手術を選択する割合は34%増加した", "figure": "BpmnTaskMessage"}], "example": "癌の外科手術の効果について死亡率の代わりに生存率が示された場合、医師が手術を選択する割合は34%増加した", "effect": "促進行動", "method": "write", "file_path": "/psy/blog/5000WRITE/5000vorcal_write/5010persuasion/2901influence.md"}, {"key": 24, "type": "Table", "question": "死亡率を提示せよ", "actions": [{"text": "", "figure": "Hammer"}, {"text": "「アクションAが仮に成功すると、プロジェクトは正常に戻りますが、25%の確率で失敗します。」", "figure": "Caution"}], "example": "「アクションAが仮に成功すると、プロジェクトは正常に戻りますが、25%の確率で失敗します。」", "effect": "回避行動", "method": "write", "file_path": "/psy/blog/5000WRITE/5000vorcal_write/5010persuasion/2901influence.md"}, {"key": 25, "type": "Table", "question": "あいまいさ回避", "actions": [{"text": "", "figure": "Hammer"}, {"text": "「６０％ぐらいです」", "figure": "Hammer"}], "example": "「６０％ぐらいです」", "effect": "回避行動", "method": "write", "file_path": "/psy/blog/5000WRITE/5000vorcal_write/5010persuasion/2901influence.md"}, {"key": 26, "type": "Table", "question": "リスクコミュニケーション", "actions": [{"text": "相手の考え方や懸念事項、それに関心の所在を正確に把握すること", "figure": "BpmnTaskMessage"}, {"text": "「よろしければこのOOに関する、一番の懸念点を教えていただけませんか？」", "figure": "Caution"}, {"text": "「もっとも負荷が高い点はどのようなことでしょうか？」", "figure": "BpmnTaskMessage"}], "example": "「よろしければこのOOに関する、一番の懸念点を教えていただけませんか？」,「もっとも負荷が高い点はどのようなことでしょうか？」", "effect": "自主的な行動の誘発,あゆみより,好感度の向上", "method": "write", "file_path": "/psy/blog/5000WRITE/5000vorcal_write/5010persuasion/conspiracy.md"}, {"key": 27, "type": "Table", "question": "「両面提示」+「反論を促す」+「それを反芻」", "actions": [{"text": "", "figure": "Caution"}, {"text": "「確かに~」", "figure": "Caution"}], "example": "「確かに~」", "effect": "十分な知識量がある相手を説得", "method": "write", "file_path": "/psy/blog/5000WRITE/5000vorcal_write/5010persuasion/2900influence.md"}, {"key": 28, "type": "Table", "question": "名詞でラベリングする", "actions": [{"text": "", "figure": "Hammer"}, {"text": "「峰岸は芸術家だ」", "figure": "Caution"}], "example": "「峰岸は芸術家だ」", "effect": "推論機能の誘発", "method": "write", "file_path": "/psy/blog/5000WRITE/5000vorcal_write/partof_speech/noun.md"}, {"key": 29, "type": "Table", "question": "ミラーリング", "actions": [{"text": "", "figure": "Caution"}, {"text": "呼吸数", "figure": "BpmnTaskMessage"}, {"text": "声の変調", "figure": "Hammer"}, {"text": "リズム", "figure": "Caution"}, {"text": "呼吸の一時停止", "figure": "Hammer"}, {"text": "動きの強さの模倣", "figure": "Caution"}], "example": "呼吸数,声の変調,リズム,呼吸の一時停止,動きの強さの模倣", "effect": "好感度の向上", "method": "write", "file_path": "/psy/blog/5000WRITE/5000vorcal_write/5000relationship/2000relationship2.md"}, {"key": 30, "type": "Table", "question": "共通点を見つける", "actions": [{"text": "ラポールの定義は、共通感です", "figure": "Hammer"}, {"text": "人は自分のような人が好きです。したがって、信頼関係を築きたい場合は、共通性を示す必要があります。", "figure": "Hammer"}, {"text": "「戦争の心理学」の中で「相手も同じ人間だ」と想像力を働かせることで、戦闘員の攻撃性が減少したのを確認しました。", "figure": "Caution"}], "example": "「戦争の心理学」の中で「相手も同じ人間だ」と想像力を働かせることで、戦闘員の攻撃性が減少したのを確認しました。", "effect": "あゆみより", "method": "write", "file_path": "/psy/blog/5000WRITE/5000vorcal_write/5000relationship/2000relationship2.md"}, {"key": 31, "type": "Table", "question": "相手の食いつきそうな話題を振る", "actions": [{"text": "", "figure": "Caution"}, {"text": "若手のエンジニアだったらフロントエンドやペアプロなどイケイケな話が好き", "figure": "Caution"}, {"text": "ベテランの歴戦の猛者なら「自分がいかにブラックな職場で無茶なやり取りをしたかの思い出」が好き", "figure": "Hammer"}], "example": "若手のエンジニアだったらフロントエンドやペアプロなどイケイケな話が好き,ベテランの歴戦の猛者なら「自分がいかにブラックな職場で無茶なやり取りをしたかの思い出」が好き", "effect": "好感度の向上", "method": "write", "file_path": "/psy/blog/5000WRITE/5000vorcal_write/5000relationship/2000relationship.md"}, {"key": 32, "type": "Table", "question": "ラベリングをする", "actions": [{"text": "", "figure": "BpmnTaskMessage"}, {"text": "「ＯＯの専門家」", "figure": "Hammer"}, {"text": "あだ名をつける", "figure": "BpmnTaskMessage"}], "example": "「ＯＯの専門家」,あだ名をつける", "effect": "自主的な行動の誘発", "method": "write", "file_path": "/psy/blog/5000WRITE/5000vorcal_write/syntax/2200unconscious.md"}, {"key": 33, "type": "Table", "question": "言語の抽象度が高い", "actions": [{"text": "", "figure": "Caution"}, {"text": "「優しい、乱暴だ」", "figure": "BpmnTaskMessage"}], "example": "「優しい、乱暴だ」", "effect": "ステレオタイプに一致,期待通り", "method": "read", "file_path": "/psy/blog/3000READ/3000vorcal_read/abstract.md"}, {"key": 34, "type": "Table", "question": "瞬きの回数が10秒に1~2回", "actions": [{"text": "", "figure": "Hammer"}, {"text": "6~10の瞬きはリラックスされたフラットな状態", "figure": "BpmnTaskMessage"}], "example": "6~10の瞬きはリラックスされたフラットな状態", "effect": "リラックス状態", "method": "read", "file_path": "/psy/blog/3000READ/3000gesture/1000read_eyes.md"}, {"key": 35, "type": "Table", "question": "極端に少ない瞬き", "actions": [{"text": "", "figure": "Hammer"}, {"text": "13人の参加者のうち10人はまばたきの回数が減りましたが、正直に話すとまばたきの頻度が通常に戻りました", "figure": "BpmnTaskMessage"}], "example": "13人の参加者のうち10人はまばたきの回数が減りましたが、正直に話すとまばたきの頻度が通常に戻りました", "effect": "嘘,緊張状態", "method": "read", "file_path": "/psy/blog/3000READ/3000gesture/1000read_eyes.md"}, {"key": 36, "type": "Table", "question": "口が少し空いている状態", "actions": [{"text": "人間は、口を開くと、内臓を見せることになります。", "figure": "Caution"}, {"text": "相手が口を開けている時は、無防備になっている状態です。", "figure": "Hammer"}], "example": "相手が口を開けている時は、無防備になっている状態です。", "effect": "リラックス状態", "method": "read", "file_path": "/psy/blog/3000READ/3000gesture/1000mouse.md"}, {"key": 37, "type": "Table", "question": "逆Uの口、くちをすくめる", "actions": [{"text": "口をすくめるのは自分の言葉に対する自信のなさ、または無力感", "figure": "BpmnTaskMessage"}, {"text": "ロバート・デ・ニーロがそのポーズを取ることで有名", "figure": "Hammer"}], "example": "ロバート・デ・ニーロがそのポーズを取ることで有名", "effect": "無関係,無力感", "method": "read", "file_path": "/psy/blog/3000READ/3000gesture/1000mouse.md"}, {"key": 38, "type": "Table", "question": "リラックス状態", "actions": [{"text": "", "figure": "Hammer"}, {"text": "最高のパフォーマンス", "figure": "BpmnTaskMessage"}], "example": "最高のパフォーマンス", "effect": "終了", "method": "read", "file_path": "/psy/blog/3000READ/null/readme.md", "category": "Terminal", "text": "リラックス状態"}, {"key": 39, "type": "Table", "question": "嘘", "actions": [{"text": "", "figure": "Caution"}, {"text": "嘘をついている状態", "figure": "BpmnTaskMessage"}], "example": "嘘をついている状態", "effect": "終了", "method": "read", "file_path": "/psy/blog/3000READ/null/readme.md", "category": "Terminal", "text": "嘘"}, {"key": 40, "type": "Table", "question": "緊張状態", "actions": [{"text": "", "figure": "Hammer"}, {"text": "緊張している状態", "figure": "Caution"}], "example": "緊張している状態", "effect": "終了", "method": "read", "file_path": "/psy/blog/3000READ/null/readme.md", "category": "Terminal", "text": "緊張状態"}, {"key": 41, "type": "Table", "question": "無関係", "actions": [{"text": "", "figure": "Caution"}, {"text": "緊張している状態", "figure": "Hammer"}], "example": "緊張している状態", "effect": "終了", "method": "read", "file_path": "/psy/blog/3000READ/null/readme.md", "category": "Terminal", "text": "無関係"}, {"key": 42, "type": "Table", "question": "無力感", "actions": [{"text": "", "figure": "Caution"}, {"text": "緊張している状態", "figure": "Caution"}], "example": "緊張している状態", "effect": "終了", "method": "read", "file_path": "/psy/blog/3000READ/null/readme.md", "category": "Terminal", "text": "無力感"}, {"key": 43, "type": "Table", "question": "好感度の向上", "actions": [{"text": "", "figure": "Hammer"}, {"text": "a", "figure": "BpmnTaskMessage"}], "example": "a", "effect": "一貫性の法則", "method": "read", "file_path": "/psy/blog/3000READ/null/readme.md"}, {"key": 44, "type": "Table", "question": "十分な知識量がある相手を説得", "actions": [{"text": "", "figure": "Hammer"}, {"text": "緊張している状態", "figure": "Caution"}], "example": "緊張している状態", "effect": "終了", "method": "read", "file_path": "/psy/blog/3000READ/null/readme.md", "category": "Terminal", "text": "十分な知識量がある相手を説得"}], "linkDataArray": [{"from": 0, "to": 21}, {"from": 5, "to": 4}, {"from": 6, "to": 0}, {"from": 7, "to": 2}, {"from": 8, "to": 1}, {"from": 9, "to": 3}, {"from": 9, "to": 4}, {"from": 12, "to": 3}, {"from": 21, "to": 22}, {"from": 22, "to": 14}, {"from": 23, "to": 20}, {"from": 24, "to": 19}, {"from": 25, "to": 19}, {"from": 26, "to": 13}, {"from": 26, "to": 18}, {"from": 26, "to": 43}, {"from": 27, "to": 44}, {"from": 28, "to": 17}, {"from": 29, "to": 43}, {"from": 30, "to": 18}, {"from": 31, "to": 43}, {"from": 32, "to": 13}, {"from": 33, "to": 15}, {"from": 33, "to": 16}, {"from": 34, "to": 38}, {"from": 35, "to": 39}, {"from": 35, "to": 40}, {"from": 36, "to": 38}, {"from": 37, "to": 41}, {"from": 37, "to": 42}, {"from": 43, "to": 22}]}`
        );
      }

      const changeTheme = () => {
        const myDiagram = go.Diagram.fromDiv('myDiagramDiv');
        if (myDiagram) {
          myDiagram.themeManager.currentTheme = document.getElementById('theme').value;
        }
      };

      const changeIsExplainOpen = () => {
        const myDiagram = go.Diagram.fromDiv('myDiagramDiv');
        if (myDiagram) {
          isExplainOpen = true
        }
        init()
      };

      window.addEventListener('DOMContentLoaded', init);
    </script>

    <div id="sample">
      <div id="myDiagramDiv" style="border: solid 1px black; width: 100%; height: 90vh"></div>
      Theme:
      <select id="theme" onchange="changeTheme()">
        <option value="system">System</option>
        <option value="light">Light</option>
        <option value="dark">Dark</option>
      </select>
      isExplainOpen:
      <select id="isExplainOpen" onchange="changeIsExplainOpen()">
        <option value="true">true</option>
        <option value="false">false</option>
      </select>
    </div>
  </div>
</body>

</html>