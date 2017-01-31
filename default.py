""" This file is the starting-point for the script(s).
	Documentation is currently only available in Swedish. Located at http://verifierad.nu - which redirects to a Github repository.

	A change-log is kept in the file CHANGELOG.md
"""

import _privatekeys as privatekeys
import test

test.mobileFriendlyCheck('http://vgregion.se/', privatekeys.googleMobileFriendlyApiKey)