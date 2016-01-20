import re
from ckan.lib.base import BaseController, c, render, request
from ckan.controllers.storage import StorageController
from ckan.controllers.user import UserController
from pylons.controllers.util import abort

from ckan.model import Session
from ckanext.qgov.data.authenticator import QGOVUser

class QGOVDataController(BaseController):
    #Data
    def mapsGeospatial(self):
        return render('static-content/maps-geospatial/index.html')

    def mapsGeospatialGlobe(self):
        return render('static-content/maps-geospatial/qld-globe/index.html')

    def requestData(self):
        return render('static-content/request-data/index.html')

    def thanks(self):
        return render('static-content/thanks/index.html')

    def otherData(self):
        return render('static-content/other-data/index.html')

    #Events
    def dataEvent(self):
        return render('static-content/data-event/index.html')

    def dataEventPremiersAwards(self):
        return render('static-content/data-event/premiers-awards/index.html')

    def dataPremierAwardEvents(self):
        return render('static-content/data-event/premiers-awards/events/index.html')

    def dataPremierAwardGuidelines(self):
        return render('static-content/data-event/premiers-awards/guidelines/index.html')

    def dataPremierAwardAbout(self):
        return render('static-content/data-event/premiers-awards/about/index.html')

    def dataPremierAwardAbout2013(self):
        return render('static-content/data-event/premiers-awards/about-2013/index.html')

    def dataEventOpeningTheVault(self):
        return render('static-content/data-event/opening-the-vault/index.html')

    def dataEventGovHack2014(self):
        return render('static-content/data-event/govhack-2014/index.html')

    def dataEventMicrosoftMasterclass(self):
        return render('static-content/data-event/microsoft-masterclass/index.html')

    #Strategies
    def departmentStrategies(self):
        return render('static-content/department-strategies/index.html')

    def departmentStrategiesAbout(self):
        return render('static-content/department-strategies/about/index.html')

    #For developers
    def forDevelopers(self):
        return render('static-content/for-developers/index.html')

    def forDevelopersRegisterYourApp(self):
        return render('static-content/for-developers/register-your-app/index.html')

    #Contact
    def contact(self):
        return render('static-content/contact/index.html')

    #Feedback
    def feedback(self):
        return render('static-content/feedback/index.html')

    #Announcements
    def announcements(self):
        return render('static-content/announcements/index.html')

    #Case Studies
    def caseStudies(self):
        return render('static-content/case-studies/index.html')

    def caseStudiesWeatherData(self):
        return render('static-content/case-studies/weather-data/index.html')

    def caseStudiesWildlifeData(self):
        return render('static-content/case-studies/wildlife-data/index.html')

    def caseStudiesMultipleSoilDatasets(self):
        return render('static-content/case-studies/multiple-soil-datasets/index.html')

    def caseStudiesQldSchoolZones(self):
        return render('static-content/case-studies/qld-school-zones/index.html')

    def caseStudiesPocketZoner(self):
        return render('static-content/case-studies/pocket-zoner/index.html')

    def caseStudiesBrisbaneBusTrainApp(self):
        return render('static-content/case-studies/brisbane-bus-train-app/index.html')

    def static_content(self, path):
        from ckan.lib.render import TemplateNotFound
        try:
            return render('static-content/'+path+'/index.html')
        except TemplateNotFound:
            from pylons import tmpl_context as c
            c.code = ['404']
            return render('error_document_template.html')

    allowedFileExtensionsRegex = r'.*((\.csv)|(\.xls)|(\.txt)|(\.kmz)|(\.xlsx)|(\.pdf)|(\.shp)|(\.tab)|(\.jp2)|(\.esri)|(\.gdb)|(\.jpg)|(\.tif)|(\.tiff)|(\.jpeg)|(\.xml)|(\.kml)|(\.doc)|(\.docx)|(\.rtf))$'

    def upload_handle(self):
        params = dict(request.params.items())
        originalFilename = params.get('file').filename
        if re.search(QGOVDataController.allowedFileExtensionsRegex, originalFilename.lower(), re.I):
            return StorageController.upload_handle(StorageController())
        abort(403, 'This file type is not supported. If possible, upload the file in another format.\nIf you continue to have problems, email Smart Service—\nonlineservices@smartservice.qld.gov.au')

    def logged_in(self):
        controller = UserController()
        if not c.user:
            # a number of failed login attempts greater than 10
            # indicates that the locked user is associated with the current request
            qgovUser = Session.query(QGOVUser).filter(QGOVUser.login_attempts > 10).first()
            if qgovUser:
                qgovUser.login_attempts = 10
                Session.commit()
                return controller.login('account-locked')
        return controller.logged_in()
