var CalibriBold = function () {
this.addFileToVFS('Calibri Bold-bold.ttf', CB);
this.addFont('Calibri Bold-bold.ttf', 'Calibri Bold', 'bold');
};
jsPDF.API.events.push(['addFonts', CalibriBold])