#!/usr/bin/env python3
"""
Smoke Test: Backend Calculation API
5-Minute Sanity Check vor Integration

Note: Uses httpx instead of requests (already in requirements.txt for pytest)
"""
import subprocess
import time
import sys
import os

# Try to import httpx, fall back to urllib if not available
try:
    import httpx as http_client
    USE_HTTPX = True
except ImportError:
    import urllib.request
    import json as json_module
    USE_HTTPX = False
    print("Warning: httpx not available, using urllib")

def get_json(url, timeout=5):
    """GET request returning JSON"""
    if USE_HTTPX:
        r = http_client.get(url, timeout=timeout)
        if r.status_code != 200:
            raise AssertionError(f"GET {url} failed: {r.status_code}")
        return r.json()
    else:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json_module.loads(response.read().decode())

def post_json(url, data, timeout=5):
    """POST request with JSON payload"""
    if USE_HTTPX:
        r = http_client.post(url, json=data, timeout=timeout)
        if r.status_code != 200:
            raise AssertionError(f"POST {url} failed: {r.status_code}")
        return r.json()
    else:
        req = urllib.request.Request(
            url,
            data=json_module.dumps(data).encode(),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json_module.loads(response.read().decode())

def main():
    print("=" * 60)
    print("🔥 SMOKE TEST: Backend Calculation API")
    print("=" * 60)

    # 1. Start FastAPI Server
    print("\n[1/5] Starting FastAPI server...")
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8001"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    print("      Waiting 5 seconds for server startup...")
    time.sleep(5)

    base_url = "http://localhost:8001"

    try:
        # 2. Health Check
        print("\n[2/5] Testing /health endpoint...")
        health_data = get_json(f"{base_url}/health")
        print(f"      ✅ Health OK: {health_data}")

        # 3. Materials Endpoint
        print("\n[3/5] Testing /api/materials endpoint...")
        materials_data = get_json(f"{base_url}/api/materials")
        materials = materials_data.get("materials", [])
        assert len(materials) == 8, f"Expected 8 materials, got {len(materials)}"
        print(f"      ✅ Materials OK ({len(materials)} materials loaded)")
        print(f"         Materials: {', '.join([m['name'] for m in materials[:3]])}...")

        # 4. Operations Endpoint
        print("\n[4/5] Testing /api/operations endpoint...")
        operations_data = get_json(f"{base_url}/api/operations")
        operations = operations_data.get("operations", [])
        total_ops = sum(len(group["operations"]) for group in operations)
        assert total_ops == 13, f"Expected 13 operations, got {total_ops}"
        print(f"      ✅ Operations OK ({total_ops} operations loaded)")
        print(f"         Categories: {', '.join([g['group'] for g in operations])}...")

        # 5. Calculation Endpoint (Full Flow: Register Tool + Calculate)
        print("\n[5/5] Testing /api/calculate endpoint...")

        # 5a. Register test tool
        print("      5a. Registering test tool...")
        tool_payload = {
            "id": "SMOKE_TEST_TOOL",
            "name": "10mm End Mill (Smoke Test)",
            "type": "flat_end_mill",
            "geometry": {
                "DC": 10.0,
                "LCF": 25.0,
                "NOF": 2,
                "DCON": 10.0,
                "OAL": 75.0,
                "SFDM": 10.0
            }
        }
        post_json(f"{base_url}/api/tools", tool_payload)
        print(f"         ✅ Tool registered")

        # 5b. Calculate
        print("      5b. Running calculation...")
        calc_payload = {
            "tool_id": "SMOKE_TEST_TOOL",
            "material": "aluminium",
            "operation": "slot_rough",
            "coating": "tin",
            "surface_quality": "standard",
            "coolant": "wet"
        }
        result = post_json(f"{base_url}/api/calculate", calc_payload)

        # Check critical fields in response structure
        assert "results" in result, "Missing 'results' in response"
        res = result["results"]

        assert "vc_final" in res, "Missing 'vc_final' in result"
        assert "n_rpm" in res, "Missing 'n_rpm' in result"
        assert "fz_final" in res, "Missing 'fz_final' in result"
        assert "vf_mm_min" in res, "Missing 'vf_mm_min' in result"
        assert "ae_mm" in res, "Missing 'ae_mm' in result"
        assert "ap_mm" in res, "Missing 'ap_mm' in result"

        print(f"      ✅ Calculate OK")
        print(f"         vc: {res['vc_final']:.1f} m/min")
        print(f"         n:  {res['n_rpm']} RPM")
        print(f"         fz: {res['fz_final']:.4f} mm")
        print(f"         vf: {res['vf_mm_min']:.1f} mm/min")
        print(f"         ae: {res['ae_mm']:.2f} mm")
        print(f"         ap: {res['ap_mm']:.2f} mm")
        print(f"         ap_reference: {res['ap_reference']}")

        # Check validation
        assert "validation" in result, "Missing 'validation' in response"
        val = result["validation"]
        assert "all_passed" in val, "Missing 'all_passed' in validation"
        assert len(val.get("checks", [])) == 8, f"Expected 8 validation checks, got {len(val.get('checks', []))}"
        print(f"      ✅ Validation: {len(val['checks'])} checks, all_passed={val['all_passed']}")

        print("\n" + "=" * 60)
        print("🎉 SMOKE TEST PASSED!")
        print("=" * 60)
        print("\n✅ All 5 checks successful:")
        print("   1. Server started")
        print("   2. Health endpoint working")
        print("   3. Materials endpoint working (8 materials)")
        print("   4. Operations endpoint working (13 operations)")
        print("   5. Calculation endpoint working (10-phase engine)")
        print(f"      - Tool registration: OK")
        print(f"      - Calculation: OK")
        print(f"      - Validation (8 checks): OK")
        print("\n✅ Backend ready for integration!")
        return 0

    except Exception as e:
        print(f"\n❌ SMOKE TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        # Stop server
        print("\n🛑 Stopping server...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
            print("   Server stopped")
        except subprocess.TimeoutExpired:
            proc.kill()
            print("   Server killed (forced)")

if __name__ == "__main__":
    sys.exit(main())
