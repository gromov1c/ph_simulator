import unittest

from src.calculations import *


# Helper function to compute H+ concentration from pH
def compute_H_concentration(pH):
    return 10 ** (-pH)


class TestCalculations(unittest.TestCase):
    def setUp(self):
        # Set up test data based on provided data (data.ods)
        self.test_data = {
            "barium_hydroxide": {"pH": 12.301, "H_concentration": 5.00E-13, "concentration": 0.01},
            "calcium_hydroxide": {"pH": 12.301, "H_concentration": 5.00E-13, "concentration": 0.01},
            "sodium_hydroxide": {"pH": 12.000, "H_concentration": 1.00E-12, "concentration": 0.01},
            "hydrochloric_acid": {"pH": 2.000, "H_concentration": 1.00E-02, "concentration": 0.01},
            "acetic_acid": {"pH": 3.372, "H_concentration": 4.24E-04, "concentration": 0.01},
            "sodium_chloride": {"pH": 7.000, "H_concentration": 1.00E-07, "concentration": 0.01},
        }

    def test_compute_pH(self):
        """Test the compute_pH function."""
        for solution, data in self.test_data.items():
            calculated_pH = ph_from_h_concentration(data["H_concentration"])
            self.assertAlmostEqual(calculated_pH, data["pH"], places=2, msg=f"Failed for {solution}")

    def test_calculate_buffer_pH(self):
        """Test calculate_buffer_pH function for known buffer systems."""
        buffer_data = {
            "acetic_acid": {"pH": 4.745, "acid_conc": 0.1, "base_conc": 0.1, "pKa": pKA_HC2H3O2},
            "ammonia": {"pH": 9.255, "acid_conc": 0.1, "base_conc": 0.1, "pKa": pKA_NH4Cl},
            "phosphate": {"pH": 7.208, "acid_conc": 0.1, "base_conc": 0.1, "pKa": pKA_NaH2PO4},
        }
        for buffer, data in buffer_data.items():
            # For a 1:1 ratio of acid:base with no titrant added (drops=0), pH = pKa
            calculated_pH = buffer_ph_general(data["acid_conc"], data["base_conc"], data["pKa"], 0.1, 0,
                                              addition='acid')
            self.assertAlmostEqual(calculated_pH, data["pH"], places=3, msg=f"Failed for {buffer}")

    def test_compute_H_concentration(self):
        """Test the compute_H_concentration function."""
        for solution, data in self.test_data.items():
            calculated_H = compute_H_concentration(data["pH"])
            self.assertAlmostEqual(calculated_H, data["H_concentration"], places=5, msg=f"Failed for {solution}")

    def test_specific_acid_base_functions(self):
        """Test specific acid and base functions."""
        # Test barium hydroxide
        h_conc = h_conc_baoh2(self.test_data["barium_hydroxide"]["concentration"])
        self.assertAlmostEqual(h_conc, self.test_data["barium_hydroxide"]["H_concentration"], places=5)

        # Test calcium hydroxide
        h_conc = h_conc_caoh2(self.test_data["calcium_hydroxide"]["concentration"])
        self.assertAlmostEqual(h_conc, self.test_data["calcium_hydroxide"]["H_concentration"], places=5)

        # Test sodium hydroxide
        h_conc = h_conc_naoh(self.test_data["sodium_hydroxide"]["concentration"])
        self.assertAlmostEqual(h_conc, self.test_data["sodium_hydroxide"]["H_concentration"], places=5)

        # Test hydrochloric acid
        h_conc = h_conc_hcl(self.test_data["hydrochloric_acid"]["concentration"])
        self.assertAlmostEqual(h_conc, self.test_data["hydrochloric_acid"]["H_concentration"], places=5)

        # Test acetic acid
        h_conc = h_conc_hc2h3o2(self.test_data["acetic_acid"]["concentration"])
        self.assertAlmostEqual(h_conc, self.test_data["acetic_acid"]["H_concentration"], places=5)

        # Test sodium chloride
        ph = ph_nacl()
        self.assertAlmostEqual(ph, self.test_data["sodium_chloride"]["pH"], places=3)

    def test_titration_functions(self):
        """Test titration functions."""
        # Test HCl titration
        h_conc = h_conc_titration_hcl(0.1, 10)
        ph = ph_from_h_concentration(h_conc)
        self.assertGreater(ph, 0)  # pH should be positive
        self.assertLess(ph, 7)  # pH should be acidic

        # Test NaOH titration
        h_conc = h_conc_titration_naoh(0.1, 10)
        ph = ph_from_h_concentration(h_conc)
        self.assertGreater(ph, 7)  # pH should be basic
        self.assertLess(ph, 14)  # pH should be less than 14

    def test_buffer_functions(self):
        """Test buffer functions."""
        # Test buffer pH calculation
        ph = buffer_ph_general(0.1, 0.1, pKA_HC2H3O2, 0.1, 0, addition='acid')
        self.assertAlmostEqual(ph, pKA_HC2H3O2, places=3)

        # Test buffer with acid addition
        ph = buffer_ph_general(0.1, 0.1, pKA_HC2H3O2, 0.1, 10, addition='acid')
        self.assertLess(ph, pKA_HC2H3O2)  # pH should decrease with acid addition

        # Test buffer with base addition
        ph = buffer_ph_general(0.1, 0.1, pKA_HC2H3O2, 0.1, 10, addition='base')
        self.assertGreater(ph, pKA_HC2H3O2)  # pH should increase with base addition

    def test_buffer_overflow(self):
        """Test buffer overflow functions."""
        # Test buffer overflow with acid
        with self.assertRaises(ValueError):
            # This should raise an error if buffer capacity is not exceeded
            buffer_overflow_ph_general('acid', 0.1, 0.1, 5)

        # Test actual overflow
        try:
            ph = buffer_overflow_ph_general('acid', 0.001, 0.1, 100)
            self.assertLess(ph, 7)  # pH should be acidic after overflow
        except ValueError:
            self.fail("buffer_overflow_ph_general raised ValueError unexpectedly")

        # Test buffer overflow with base
        with self.assertRaises(ValueError):
            # This should raise an error if buffer capacity is not exceeded
            buffer_overflow_ph_general('base', 0.1, 0.1, 5)

        # Test actual overflow
        try:
            ph = buffer_overflow_ph_general('base', 0.001, 0.1, 100)
            self.assertGreater(ph, 7)  # pH should be basic after overflow
        except ValueError:
            self.fail("buffer_overflow_ph_general raised ValueError unexpectedly")


if __name__ == '__main__':
    unittest.main()
