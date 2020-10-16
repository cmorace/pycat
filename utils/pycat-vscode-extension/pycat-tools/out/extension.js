"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require("vscode");
const config = vscode.workspace.getConfiguration('pycat-tools');
const python = config.get('pythonPath');
// const python = '/Volumes/Transcend/Work/Peanuts/pycat-master/.env/bin/python3.8';
const path = require('path');
const { spawn } = require('child_process');
const editorFile = path.join(__dirname, '/image_editor_extended.py');
const autoCropFile = path.join(__dirname, '/image_auto_crop_extended.py');
// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
function activate(context) {
    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, "pycat-tools" is now active!');
    console.log(python);
    // The command has been defined in the package.json file
    // Now provide the implementation of the command with registerCommand
    // The commandId parameter must match the command field in package.json
    let editor = vscode.commands.registerCommand('pycat-tools.openEditor', (e) => {
        console.log("pycat-tools: opening image editor");
        const process = spawn(python, [editorFile, e.fsPath]);
        process.stdout.on('data', function (data) {
            console.log(data.toString());
        });
        process.on('close', (code) => {
            console.log("pycat-tools: closing image editor");
        });
    });
    let autoCrop = vscode.commands.registerCommand('pycat-tools.autoCrop', (e) => {
        console.log("pycat-tools: running auto-crop");
        const process = spawn(python, [autoCropFile, e.fsPath]);
        process.stdout.on('data', function (data) {
            console.log(data.toString());
        });
        process.on('close', (code) => {
            console.log("pycat-tools: closing auto-crop");
        });
    });
    context.subscriptions.push(autoCrop);
    context.subscriptions.push(editor);
}
exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map