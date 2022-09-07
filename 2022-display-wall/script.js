const wallWidth = 10;
const wallHeight = 6;

const palletColors = [
    '#cc0000', // red
    '#ffff66', // yellow
    '#3399ff', // blue
    '#33cc33', // green
    '#e8e8e8', // gray
    '#ffffff', // white
    '#000000', // black
    '#e6f2ff', // translucent blue
    '#ffffff' // white with red swirl
]

let currentColor = '#cc0000';

function pickColor(color) {
    currentColor = color;
}

function setPixelColor(pixel) {
    pixel.style.backgroundColor = currentColor;
    updateCode();
}

function updateCode() {
    const wall = document.getElementById('wall');
    const code = document.getElementById('code');
    code.innerText = format(wall, 0).innerHTML;
    code.innerHTML = removeBlanks(code);
}

function removeBlanks(node) {
    const withoutBlanks = [];
    node.innerHTML.split('<br>').forEach(originalLine => {
        if (originalLine.trim() != "") {
            withoutBlanks.push(originalLine);
        }
    })

    return withoutBlanks.join('\n');
}

function format(node, level) {
    const indentBefore = new Array(level++ + 1).join('  ');
    const indentAfter = new Array(level - 1).join('  ');
    let textNode;

    for (let i = 0; i < node.children.length; i++) {
        textNode = document.createTextNode('\n' + indentBefore);
        node.insertBefore(textNode, node.children[i]);

        format(node.children[i], level);

        if (node.lastElementChild == node.children[i]) {
            textNode = document.createTextNode('\n' + indentAfter);
            node.appendChild(textNode);
        }
    }

    return node;
}

function initializeWall() {
    const wall = document.getElementById('wall');

    let rowTemplate = document.createElement('div');
    rowTemplate.classList.add('row');
    let pixelTemplate = document.createElement('div');
    pixelTemplate.classList.add('pixel');

    for (let col = 0; col < wallWidth; col++) {
        rowTemplate.appendChild(pixelTemplate.cloneNode(true));
    }

    for (let row = 0; row < wallHeight; row++) {
        wall.appendChild(rowTemplate.cloneNode(true));
    }

    document.querySelectorAll('.pixel').forEach(pixel => {
        pixel.onclick = function () {
            setPixelColor(this);
        };
    });
}

function initializePallet() {
    const pallet = document.getElementById('pallet');
    const palletItemTemplate = document.createElement('div');
    palletItemTemplate.classList.add('pallet');
    palletColors.forEach(color => {
        let palletItem = palletItemTemplate.cloneNode(true);
        palletItem.style.backgroundColor = color;
        palletItem.onclick = function () {
            pickColor(color);
        };
        pallet.appendChild(palletItem);
    });
}