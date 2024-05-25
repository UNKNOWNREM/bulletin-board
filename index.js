const express = require('express');
const path = require('path');
const app = express();

// 指向静态文件目录
const publicDir = path.join(__dirname, 'public');
app.use(express.static(publicDir));

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`服务器运行在 http://localhost:${PORT}`);
});