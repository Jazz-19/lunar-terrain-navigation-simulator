import cv2
import numpy as np
import glob
import os

def process_lunar_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None, "Error Loading Image"

    height, width = img.shape[:2]

    # 1. Preprocessing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    smoothed = cv2.GaussianBlur(gray, (7, 7), 2.0)

    # 2. Horizon Masking (Ignore top 30% sky/horizon)
    ground_mask = np.ones((height, width), dtype=np.uint8)
    ground_mask[0:int(height * 0.30), :] = 0

    # 3. Surface Roughness Detection via Gradient
    kernel_5x5 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    range_map = cv2.morphologyEx(smoothed, cv2.MORPH_GRADIENT, kernel_5x5)

    # Normalize range map
    range_max = np.max(range_map)
    range_norm = range_map.astype(np.float32) / (range_max if range_max > 0 else 1)

    # 4. Adaptive Thresholding for Hazard Detection
    # Dynamic cutoff based on average terrain texture
    mean_roughness = np.mean(range_norm[ground_mask == 1])
    t_factor = mean_roughness * 0.85  # Adaptive cutoff

    walkable_raw = ((range_norm < t_factor) & (ground_mask == 1)).astype(np.uint8) * 255

    # Morphological cleaning
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    walkable_clean = cv2.morphologyEx(walkable_raw, cv2.MORPH_CLOSE, kernel_close)

    # Filter small noise patches
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(walkable_clean)
    walkable_filtered = np.zeros_like(walkable_clean)
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] >= 800:
            walkable_filtered[labels == i] = 255

    # 5. Three-Corridor Navigation Analysis (Lower 45% ROI)
    roi_start = int(height * 0.55)
    roi = walkable_filtered[roi_start:, :]
    roi_h, roi_w = roi.shape

    # Split bottom view into 3 equal columns: Left, Center, Right
    col_w = roi_w // 3
    left_zone = roi[:, :col_w]
    center_zone = roi[:, col_w:2*col_w]
    right_zone = roi[:, 2*col_w:]

    # Calculate safe pixel ratio in each sector
    left_score = np.sum(left_zone == 255)
    center_score = np.sum(center_zone == 255)
    right_score = np.sum(right_zone == 255)

    total_safe_pixels = left_score + center_score + right_score

    # Steering Decision Logic based on clearest corridor
    if total_safe_pixels < (roi_h * roi_w * 0.05):
        nav_status = "STOP - Obstacle Ahead!"
        command_color = (0, 0, 255) # Red
        target_x = int(width / 2)
    else:
        # Determine safest corridor
        scores = {"Drive STRAIGHT": center_score, "Steer LEFT": left_score, "Steer RIGHT": right_score}
        nav_status = max(scores, key=scores.get)

        if nav_status == "Drive STRAIGHT":
            target_x = int(width * 0.5)
            command_color = (0, 255, 0) # Green
        elif nav_status == "Steer LEFT":
            target_x = int(width * 0.25)
            command_color = (0, 255, 255) # Yellow
        else:
            target_x = int(width * 0.75)
            command_color = (0, 255, 255) # Yellow

    # 6. Visualization Overlay
    output_img = img.copy()
    green_overlay = np.zeros_like(img)
    green_overlay[walkable_filtered == 255] = [0, 255, 0]
    output_img = cv2.addWeighted(output_img, 0.7, green_overlay, 0.45, 0)

    # Draw Corridor Boundary Lines on screen
    cv2.line(output_img, (col_w, roi_start), (col_w, height), (255, 255, 255), 1)
    cv2.line(output_img, (2 * col_w, roi_start), (2 * col_w, height), (255, 255, 255), 1)

    # Draw Steering Vector Line & Indicator
    target_y = height - 40
    cv2.line(output_img, (int(width / 2), height), (target_x, target_y), (0, 0, 255), 3)
    cv2.circle(output_img, (target_x, target_y), 8, (0, 0, 255), -1)

    return output_img, nav_status, command_color

def run_demo(folder_path=os.path.join("dataset", "render"), delay_seconds=5):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_folder = os.path.join(script_dir, folder_path)

    image_paths = []
    for ext in ('*.png', '*.jpg', '*.jpeg'):
        image_paths.extend(glob.glob(os.path.join(target_folder, ext)))

    if not image_paths:
        print(f"[ERROR] No images found in '{target_folder}'!")
        return

    print(f"\n==================================================")
    print(f" LUNAR ROVER AUTONOMOUS NAVIGATION DEMO ACTIVATED ")
    print(f" Loaded {len(image_paths)} images from dataset/render.")
    print(f" Delay per image: {delay_seconds} seconds")
    print(f" [CONTROLS]:")
    print(f"   - Press 'q' or 'Esc' to EXIT")
    print(f"   - Press 'SPACEBAR' to PAUSE / RESUME")
    print(f"==================================================\n")

    try:
        for idx, path in enumerate(image_paths):
            filename = os.path.basename(path)
            result = process_lunar_image(path)

            if result[0] is None:
                continue

            result_frame, command, cmd_color = result

            print(f" Frame [{idx+1}/{len(image_paths)}] | File: {filename} --> Command: {command}")

            # Render On-Screen Display
            cv2.putText(result_frame, f"Frame: {filename}", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(result_frame, f"Nav Command: {command}", (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, cmd_color, 2)
            cv2.putText(result_frame, "[Q] Quit  |  [SPACE] Pause/Resume", (20, result_frame.shape[0] - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 220, 220), 1)

            cv2.imshow("Autonomous Lunar Navigation Feed", result_frame)

            # Wait Key Control
            key = cv2.waitKey(int(delay_seconds * 1000)) & 0xFF

            if key == ord('q') or key == 27:
                print("\n[STOPPED] Demo exited by user.")
                break

            elif key == 32: # Spacebar Pause
                print("\n[PAUSED] Press SPACEBAR to resume...")
                while True:
                    pause_key = cv2.waitKey(100) & 0xFF
                    if pause_key == 32:
                        print("[RESUMED] Continuing...\n")
                        break
                    elif pause_key == ord('q') or pause_key == 27:
                        cv2.destroyAllWindows()
                        return

    
    except KeyboardInterrupt:
        print("\n[STOPPED] Terminated by terminal.")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Adjust delay_seconds here (currently set to 5 seconds per image)
    run_demo(folder_path=os.path.join("Images"), delay_seconds=5)
