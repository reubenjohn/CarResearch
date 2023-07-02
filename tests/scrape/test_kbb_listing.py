from unittest import TestCase

from car_researcher.scrape.kbb_listing import KBBListing, Mileage, scrape_kbb_listing, VehicleFeature
from tests.scrape.fetch import StatelessTestVectorFetcher


class Test(TestCase):
    def test_scrape_kbb_listing(self):
        listing = scrape_kbb_listing('kbb_listing', StatelessTestVectorFetcher())
        self.assertEqual(listing, KBBListing(43_293, 'Hybrid: Gas/Electric', Mileage(43, 37), 'All wheel drive',
                                             'Continuously Variable Automatic Transmission', EXPECTED_VEHICLE_FEATURES))


EXPECTED_VEHICLE_FEATURES = [
    VehicleFeature('Exterior', [
        'Alloy wheels', 'Auto High-beam Headlights', 'Black Roof-Rack Side Rails', 'Bumpers: body-color',
        'Delay-off headlights', 'Front fog lights', 'Fully automatic headlights', 'Heated door mirrors',
        'Power door mirrors', 'Rear window wiper', 'Spoiler', 'Turn signal indicator mirrors',
        'Wheels: 19" Machined-Face Aluminum']),
    VehicleFeature('Interior', [
        'Air Conditioning', 'Auto-dimming Rear-View mirror', 'Driver door bin', 'Driver vanity mirror',
        'Front Bucket Seats', 'Front Center Armrest', 'Front dual zone A/C', 'Front reading lights',
        'Garage door transmitter', 'Heated front seats', 'Heated steering wheel', 'Leather steering wheel',
        'Memory seat', 'Overhead console', 'Panoramic Vista Roof', 'Passenger door bin', 'Passenger vanity mirror',
        'Power Liftgate', 'Power driver seat', 'Power passenger seat', 'Power windows', 'Rear reading lights',
        'Rear seat center armrest', 'Rear window defroster', 'Speed-Sensitive Wipers', 'Split folding rear seat',
        'Steering wheel mounted audio controls', 'Telescoping steering wheel', 'Tilt steering wheel', 'Trip computer',
        'Variably intermittent wipers']),
    VehicleFeature('Safety', [
        'ABS brakes', 'Brake assist', 'Dual front impact airbags', 'Dual front side impact airbags',
        'Electronic Stability Control', 'Electronic Stability Control / ESC / Traction Control',
        'Emergency communication system: SYNC 3 911 Assist', 'Knee airbag', 'Low tire pressure warning',
        'Occupant sensing airbag', 'Overhead airbag', 'Panic alarm', 'Security system', 'Traction control']),
    VehicleFeature('Mechanical', [
        '2.91 Axle Ratio', '4-Wheel Disc Brakes', 'Four wheel independent suspension', 'Power steering',
        'Speed-sensing steering']),
    VehicleFeature('Technology', [
        '10 Speakers', 'AM/FM radio: SiriusXM', 'Automatic temperature control', 'Compass',
        'Exterior Parking Camera Rear', 'Head-Up Display', 'Navigation System', 'Radio data system',
        'Radio: B&O Sound System by Bang & Olufsen', 'Rain sensing wipers', 'Remote keyless entry',
        'SYNC 3 Communications & Entertainment System', 'Speed control',
        'Voice-Activated Touchscreen Navigation System']),
    VehicleFeature('Other', [
        'Active Parking Assist / Park Assist / Parking Assistance', 'All-Wheel Drive / Four-Wheel Drive / AWD / 4WD',
        'Alloy Wheels / Aluminum Wheels / Premium Wheels', 'AppLink/Apple CarPlay and Android Auto',
        'Apple CarPlay / Android Auto / Smartphone Integration / CarPlay',
        'Auto-Dimming Rearview Mirror / Auto-Dimming Mirror / Electrochromic Mirror',
        'Automatic Collision Avoidance / Collision Warning System / Pre-Collision System',
        'Automatic Headlights / Auto Headlights / Auto-On Headlights', 'Backup Camera / Rear Camera / Rearview Camera',
        'Blind Spot Monitor / Blind Spot Detection / BLIS', 'Bluetooth / Bluetooth Connectivity / Bluetooth Interface',
        'Dual-Zone Climate Control / Automatic Climate Control / Multi-Zone Climate Control', 'Equipment Group 400A',
        'FordPass Connect', 'Front anti-roll bar', 'Heads-Up Display / HUD / Head-Up Display',
        'Heated Leather-Trimmed Front Sport Contour Seats', 'Heated Seats / Heat Seats / Seat Warmers',
        'Illuminated entry', 'Keyless Entry / Keyless Access / Proximity Key',
        'Lane Departure Warning / Lane Departure Alert / Lane Keeping Assist',
        'Leather Seats / Leather Upholstery / Leather Interior',
        'Multi-Function Steering Wheel / Steering Wheel Controls / Steering Wheel Audio Controls',
        'Outside temperature display', 'Pedestrian Alert Sounder',
        'Power Liftgate / Hands-Free Liftgate / Automatic Tailgate',
        'Power Seats / Power Adjustable Seats / Electric Seats', 'Push-Button Start / Keyless Start / Keyless Ignition',
        'Rain-Sensing Wipers / Automatic Wipers / Rain-Sensitive Wipers',
        'Rear Cross Traffic Alert / Cross Traffic Alert / Rear Traffic Alert', 'Rear anti-roll bar',
        'Remote Start / Remote Engine Start / Remote Car Starter', 'Roof rack: rails only',
        'Smartphone App Integration / Mobile App Integration / App-Connected Features',
        'Sunroof / Moonroof / Panoramic Roof / Panoramic Sunroof', 'Titanium Premium Package (Discontinued)',
        'Voice Recognition / Voice Control / Voice Commands', 'Wireless Charging Pad']),
    VehicleFeature('Titanium Premium Package (Discontinued)', [
        'power open/close w/power shade', 'Panoramic Vista Roof', 'Head-Up Display',
        'Includes Black Roof-Rack Side Rails'])]
