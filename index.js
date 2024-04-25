const express = require('express');
const fs = require('fs');

const app = express();
const dataFile = 'data.json';
const countFile = 'count.json';

app.use(express.json());

const loadData = () => {
    try {
        const data = fs.readFileSync(dataFile);
        return JSON.parse(data);
    } catch (error) {
        return {};
    }
};

const saveData = (data) => {
    fs.writeFileSync(dataFile, JSON.stringify(data));
};

const loadCount = () => {
    try {
        const count = fs.readFileSync(countFile);
        return JSON.parse(count);
    } catch (error) {
        return { add: 0, update: 0 };
    }
};

const saveCount = (count) => {
    fs.writeFileSync(countFile, JSON.stringify(count));
};

app.post('/add', (req, res) => {
    try {
        const data = req.body;
        console.log(data);
        saveData([data]);
        // Update count for "add" operation
        const count = loadCount();
        count.add += 1;
        saveCount(count);
        res.send('Data added successfully.');
    } catch (error) {
        console.error('this is error', error);
        res.status(500).send('Internal Server Error');
    }
});

app.put('/update', (req, res) => {
    try {
        const data = req.body;
        let existingData = loadData();
        existingData.push(data);
        saveData(existingData);
        // Update count for "update" operation
        const count = loadCount();
        count.update += 1;
        saveCount(count);
        res.send('Data updated successfully.');
    } catch (error) {
        console.error('this is error', error);
        res.status(500).send('Internal Server Error');
    }
});

app.get('/count', (req, res) => {
    const count = loadCount();
    res.json(count);
});

// create file if it doesn't exist "data.json" && "count.json"
if (!fs.existsSync(dataFile)) {
    saveData([]);
}
if (!fs.existsSync(countFile)) {
    saveCount({ add: 0, update: 0 });
}

app.listen(3000, () => {
    console.log(`Example app listening at http://localhost:3000`);
});
