#include <stdio.h>
#include <windows.h>

// Function to handle double clicks at a series of x, y positions
__declspec(dllexport) void double_click_mouse(int* positions, int n) {
    for (int i = 0; i < n; i++) {
        int x = positions[i * 2];       // Even-indexed values for x
        int y = positions[i * 2 + 1];   // Odd-indexed values for y
        SetCursorPos(x, y);              // Move mouse to position

        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0); // Press
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);   // Release
        Sleep(50); // Short delay between press/release for double-click effect

        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0); // Press again
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);   // Release again
        Sleep(50); // Short delay between press/release for double-click effect
    }
}
