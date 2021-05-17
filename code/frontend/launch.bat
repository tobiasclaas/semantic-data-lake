@ECHO off
cd /D "%~dp0"
WHERE node 1>NUL 2>NUL
IF %ERRORLEVEL% NEQ 0 (
	ECHO Node.js is required to run this app but could not be found. please install Node.js and try again. 
	GOTO complete
)
echo Installing packages..
CALL npm install --silent --no-progress --dev yarn 1>NUL
CALL yarn 1>NUL 2>NUL

IF "%1" == "dev" (
	echo Building [dev]..
	CALL yarn run dev
) ELSE (
	echo Building..
	CALL yarn run build 1>NUL
)
echo Completed
:complete