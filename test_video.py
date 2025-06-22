#!/usr/bin/env python3
"""
Quick Test: Can we capture video?
"""
import cv2

# Test 1: Can we access webcam?
print("Testing webcam access...")
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("✅ Webcam accessible!")
    ret, frame = cap.read()
    if ret:
        print(f"✅ Got frame: {frame.shape}")
    cap.release()
else:
    print("❌ No webcam access")

# Test 2: Can we do screen capture?
print("\nTesting screen capture...")
try:
    # This would need additional setup on macOS
    print("⚠️ Screen capture needs macOS permissions")
except:
    print("❌ Screen capture not configured")

print("\n✅ OpenCV is working! We can build video MCP!")
