# Copyright (c) 2008, Stephen Hansen
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright 
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <ORGANIZATION> nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

from setuptools import find_packages, setup

setup(
    name = 'BlackMagicTicketTweaks', 
    version = '0.1',
    author = 'Stephen Hansen',
    author_email = 'shansen@advpubtech.com',
    description = "Various simple hacks to alter the behavior of the Ticket forms..",
    license = \
    """Copyright (c) 2008, Stephen Hansen. All rights reserved. Released under the 3-clause BSD license. """,
    url = "http://trac-hacks.org/wiki/BlackMagicTicketTweaks",
    packages = find_packages(exclude=['*.tests*']),
    package_data = {'blackmagic' : ['templates/*.html', 'htdocs/js/*.js', 'htdocs/css/*.css']}, 
    install_requires = [
        #'trac>=0.11',
    ],
    entry_points = {
        'trac.plugins': [
            'blackmagic = blackmagic',

        ]    
    }
)
