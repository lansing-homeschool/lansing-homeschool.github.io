const wallWidth = 10;
const wallHeight = 6;

const decorationsList = [
    { 'image': 'black-circle', 'count': 5 },
    { 'image': 'black-quarter', 'count': 11 },
    { 'image': 'black-square', 'count': 11 },
    { 'image': 'blue-quarter', 'count': 11 },
    { 'image': 'blue-square', 'count': 11 },
    { 'image': 'crystal-circle', 'count': 5 },
    { 'image': 'gray-quarter', 'count': 10 },
    { 'image': 'gray-square', 'count': 11 },
    { 'image': 'gray-tombstone', 'count': 5 },
    { 'image': 'green-quarter', 'count': 11 },
    { 'image': 'green-square', 'count': 11 },
    { 'image': 'green-tombstone', 'count': 5 },
    { 'image': 'orange-heart', 'count': 5 },
    { 'image': 'orange-quarter', 'count': 11 },
    { 'image': 'orange-square', 'count': 11 },
    { 'image': 'red-quarter', 'count': 11 },
    { 'image': 'red-square', 'count': 11 },
    { 'image': 'spiral-circle', 'count': 5 },
    { 'image': 'white-stud', 'count': 5 },
    { 'image': 'yellow-flower', 'count': 5 },
    { 'image': 'yellow-quarter', 'count': 11 },
    { 'image': 'yellow-square', 'count': 11 }
];

let currentDecoration = decorationsList[0];

function pickDecoration(decoration) {
    currentDecoration = decoration;
}

function setPixelImage(pixel) {
    if (currentDecoration.image === 'eraser') {
        pixel.style.backgroundImage = '';
    } else {
        const newImageUrl = `url("images/${currentDecoration.image}.png")`;
        if (newImageUrl === pixel.style.backgroundImage) {
            const currentRotation = pixel.style.transform;
            let newRotation = 'rotate(90deg)';
            if (currentRotation === 'rotate(90deg)') {
                newRotation = 'rotate(180deg)';
            } else if (currentRotation === 'rotate(180deg)') {
                newRotation = 'rotate(270deg)';
            } else if (currentRotation === 'rotate(270deg)') {
                newRotation = '';
            }
            pixel.style.transform = newRotation;
        } else {
            pixel.style.backgroundImage = `url("images/${currentDecoration.image}.png")`;
        }
    }
    updateCode();
}

function updateCode() {
    const wall = document.getElementById('wall');
    const code = document.getElementById('code');
    code.innerText = format(wall, 0).innerHTML;
    code.innerHTML = removeBlanks(code);
    document.getElementById('code-wrapper').style.display = 'inline'
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
            setPixelImage(this);
        };
    });
}

function initializeDecorations() {
    const decorations = document.getElementById('decorations');
    const decorationTemplate = document.createElement('div');
    let decorationItem;
    decorationTemplate.classList.add('decoration');
    decorationsList.forEach(decoration => {
        decorationItem = decorationTemplate.cloneNode(true);
        decorationItem.innerHTML = '&nbsp;';
        decorationItem.style.backgroundImage = `url("images/${decoration.image}.png")`;
        decorationItem.onclick = function () {
            pickDecoration(decoration);
        };
        decorations.appendChild(decorationItem);
    });
    decorationItem = decorationTemplate.cloneNode(true);
    decorationItem.innerHTML = '<span style="position: relative; top: 20px;">(eraser)</span>';
    decorationItem.onclick = function () {
        pickDecoration({ 'image': 'eraser', 'count': (wallHeight * wallWidth) });
    };
    decorations.appendChild(decorationItem);
}
