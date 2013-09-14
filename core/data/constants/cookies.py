import operator

GENERIC_COOKIES = set(['JServSessionID',
                       'JWSESSIONID',
                       'SESSID',
                       'SESSION',
                       'session_id'])


COOKIE_FINGERPRINT = (
        ('st8id', 'Teros web application firewall'),
        ('ASINFO', 'F5 TrafficShield'),
        ('NCI__SessionId', 'Netcontinuum'),

        # oracle
        ('$OC4J_', 'Oracle container for java'),

        # Java
        ('JSESSIONID', 'Jakarta Tomcat / Apache'),
        ('JServSessionIdroot', 'Apache JServ'),

        # ASP
        ('ASPSESSIONID', 'ASP'),
        ('ASP.NET_SessionId', 'ASP.NET'),

        # PHP
        ('PHPSESSID', 'PHP'),
        ('PHPSESSION', 'PHP'),

        # SAP
        ('sap-usercontext=sap-language=', 'SAP'),

        # Others
        ('WebLogicSession', 'BEA Logic'),
        ('SaneID', 'Sane NetTracker'),
        ('ssuid', 'Vignette'),
        ('vgnvisitor', 'Vignette'),
        ('SESSION_ID', 'IBM Net.Commerce'),
        ('NSES40Session', 'Netscape Enterprise Server'),
        ('iPlanetUserId', 'iPlanet'),
        ('RMID', 'RealMedia OpenADStream'),
        ('cftoken', 'Coldfusion'),
        ('PORTAL-PSJSESSIONID', 'PeopleSoft'),
        ('WEBTRENDS_ID', 'WebTrends'),
        ('sesessionid', 'IBM WebSphere'),
        ('CGISESSID', 'Perl CGI::Session'),
        ('GX_SESSION_ID', 'GeneXus'),
        ('SESSIONID', 'Apache'),
        ('WC_SESSION_ESTABLISHED', 'WSStore'),

    )

ALL_COOKIES = set(map(operator.itemgetter(0), COOKIE_FINGERPRINT))
ALL_COOKIES.update(GENERIC_COOKIES)

