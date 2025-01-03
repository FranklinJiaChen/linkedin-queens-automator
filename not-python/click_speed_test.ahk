CoordMode, Mouse, Screen
SetBatchLines, -1
SetWinDelay, -1

startTime := A_TickCount

Loop, 100
{
    Random, x, 800, 1425
    Random, y, 400, 1030
    Click %x%, %y% 2  ; DoubleClick
}

elapsedTime := (A_TickCount - startTime) / 1000
MsgBox, Time taken: %elapsedTime% seconds.`nClicks per second: % (100 / elapsedTime)
