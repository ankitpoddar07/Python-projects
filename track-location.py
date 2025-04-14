import geocoder
import gps
import time
import phonenumbers
from phonenumbers import geocoder as phone_geocoder
from gps import *

def get_location_by_ip():
    try:
        g = geocoder.ip('me')
        if g.ok:
            print("\nCurrent Location (IP-Based):")
            print("=" * 30)
            print(f"Address: {g.address}")
            print(f"Coordinates: {g.latlng[0]:.6f}, {g.latlng[1]:.6f}")
            print(f"City: {g.city}")
            print(f"Country: {g.country}")
            return g.latlng
        else:
            print("Could not fetch IP-based location.")
            return None
    except Exception as e:
        print(f"IP Location Error: {e}")
        return None

def get_location_by_gps(timeout=30):
    try:
        session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        start_time = time.time()
        last_print = 0

        print("\nAttempting to get GPS fix...")
        print("Make sure you have clear view of the sky and GPS is enabled")

        while time.time() - start_time < timeout:
            try:
                report = session.next()

                if time.time() - last_print > 5:
                    if report['class'] == 'SKY':
                        print(f"\nSatellites in view: {len(report.satellites)}")
                    last_print = time.time()

                if report['class'] == 'TPV':
                    if hasattr(report, 'mode') and report.mode >= 2:
                        if hasattr(report, 'lat') and hasattr(report, 'lon'):
                            print("\nCurrent Location (GPS):")
                            print("=" * 30)
                            print(f"Coordinates: {report.lat:.6f}, {report.lon:.6f}")
                            print(f"Mode: {report.mode}")
                            if hasattr(report, 'epx') and hasattr(report, 'epy'):
                                print(f"Estimated error: ±{max(report.epx, report.epy):.1f} meters")
                            if hasattr(report, 'speed'):
                                print(f"Speed: {report.speed:.2f} m/s")
                            if hasattr(report, 'alt'):
                                print(f"Altitude: {report.alt:.2f} m")
                            if hasattr(report, 'time'):
                                print(f"Time: {report.time}")
                            return (report.lat, report.lon)
                    else:
                        print(f"\nWaiting for GPS fix (current mode: {report.mode})...")

            except StopIteration:
                print("GPS connection lost")
                break
            except Exception as e:
                print(f"GPS reading error: {str(e)}")
                continue

        print("\nGPS timeout reached without getting a valid fix.")
        return None

    except Exception as e:
        print(f"GPS Setup Error: {e}")
        return None
    finally:
        try:
            session.close()
        except:
            pass

def get_phone_number_location(phone_number_str):
    """Get approximate location and coordinates of a phone number"""
    try:
        phone_number = phonenumbers.parse(phone_number_str)
        region_name = phone_geocoder.description_for_number(phone_number, "en")

        print("\nPhone Number Location:")
        print("=" * 30)
        print(f"Phone Number: {phone_number_str}")
        print(f"Region: {region_name}")
        print("Note: This is the registered location of the number, not current device location")

        # Now try to get coordinates of the region using geocoder
        if region_name:
            g = geocoder.osm(region_name)
            if g.ok:
                print(f"Approx Coordinates: {g.latlng[0]:.6f}, {g.latlng[1]:.6f}")
            else:
                print("Could not get coordinates for the region")
        else:
            print("Could not identify region")

    except Exception as e:
        print(f"Phone number location error: {e}")

if __name__ == "__main__":
    print("Fetching device location...")

    gps_location = get_location_by_gps(timeout=60)

    if gps_location is None:
        print("\nFalling back to IP-based location...")
        ip_location = get_location_by_ip()

    print("\nLocation retrieval complete.")

    # Change phone number here
    get_phone_number_location("+91 ")
