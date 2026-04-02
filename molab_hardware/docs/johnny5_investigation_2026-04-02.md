# johnny5 Axis PTZ Camera Investigation — 2026-04-02

Issue: rolker/mobile_lab#1

## Camera Identity
- Model: AXIS Q6215-LE PTZ Network Camera
- IP: 192.168.50.55 (johnny5.p11.lan on mobile lab 192.168.50.0/24)
- VAPIX API: responding, anonymous access (no auth required)

## Firmware
- Previous: AXIS OS 11.11.141 (built Mar 03 2025)
- Updated to: AXIS OS 11.11.192 (built Jan 17 2026)
- AXIS OS 12.x not available for Q6215-LE (hardware not supported)
- Update performed via web UI on 2026-04-02

## SSH Access
- Enabled via web UI, connected as root
- OS: AXIS OS 11.11.192 (Yocto/scarthgap), armv7l

## PTZ Capabilities (from VAPIX)
- Full absolute pan/tilt/zoom support
- Pan range: -180 to 180
- Tilt range: -90 to 90
- Zoom range: 1 to 9999
- Field angle: 20 to 575 (0.2° to 57.5°)
- Home position: pan=0, tilt=-45, zoom=1
- PTZ operator access: anonymous

## ROS Launch File Review
- File: `molab_hardware/launch/johnny5_launch.py`
- Uses `axis_camera` package, includes `axis_camera.launch`
- PTZ config: `axis_q62.yaml` (correct for Q6215-LE)
- Stream: 1920x1080 @ 15fps
- Namespace: `molab/johnny5`
- Features enabled: PTZ, IR, wiper, defog
- Bug: typo on line 55 — `enalble_ptz` should be `enable_ptz`
- Commented-out ROS1 XML launch references `axis_tracker` package and RTSP stream

## Installed ACAP Packages
- fenceguard — virtual fence detection
- loiteringguard — loitering detection
- motionguard — motion detection
- vmd — video motion detection

## Built-in Autotracking
- Motion-based autotracker present (`/usr/bin/motiontracking` daemon)
- Currently not running (`AutoTracking.A0.Running=no`)
- Supports pan/tilt limits, auto-zoom, sensitivity (High/Medium/Low)
- This is visual motion tracking — not GPS-based

## PTZ Control Verified
- VAPIX `ptz.cgi?query=position` works from localhost
- Current position at time of check: pan=66.80, tilt=-8.11, zoom=1
- Autofocus and autoiris enabled
- PTZ commands can be sent via `ptz.cgi?pan=X&tilt=Y&zoom=Z`

## Wiper Control
- NOT via PTZ auxiliary command (auxiliary=wiper returns "invalid value")
- Uses Clear View Control API: POST to `/axis-cgi/clearviewcontrol.cgi`
- Requires digest authentication (root credentials)
- Start: `{"apiVersion":"1.0","method":"start","params":{"id":0}}`
- Stop: `{"apiVersion":"1.0","method":"stop","params":{"id":0}}`
- Uses `libwiper` plugin, one-shot action with configurable duration
- API returns success but wiper not visually observed — may need physical inspection

## Auto-Tracking Feasibility (GPS-based)
For pointing camera at BizzyBoat given GPS positions:
1. Camera position: fixed lat/lon/height on mobile lab roof (height ~4m per mobile_lab.yaml)
2. Subscribe to BizzyBoat GPS position (via ROS topic or UDP bridge)
3. Compute bearing (→ pan) and elevation angle (→ tilt) from camera to boat
4. Send absolute PTZ commands via VAPIX API
5. AXIS OS 12.7+ has built-in PTZ autotracker that may simplify this

## Next Steps
- [ ] Update firmware (consider 12.x for built-in autotracker + security patches)
- [ ] Fix typo in launch file (`enalble_ptz` → `enable_ptz`)
- [ ] Test axis_camera ROS package with johnny5
- [ ] Document camera's fixed position (lat/lon) for GPS-based tracking
- [ ] Implement GPS-to-PTZ node or evaluate AXIS 12.7 autotracker
