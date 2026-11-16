/**
 * Chessopia registrations -> Google Sheet (+ optional email alert).
 * Setup: see README.md ("Store registrations in a Google Sheet").
 */
var SHEET_NAME = 'Registrations';
var NOTIFY_EMAIL = '';   // optional: your email for an alert on each new registration
var HEADERS = ['Received (IST)', 'Child name', 'Parent name', 'Phone', 'Age', 'Location', 'Batch', 'Status', 'Notes'];

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var d = JSON.parse(e.postData.contents);
    if (d.website) return out({ok: true});            // honeypot: bots fill this, ignore silently
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    if (sh.getLastRow() === 0) {
      sh.appendRow(HEADERS);
      sh.setFrozenRows(1);
      sh.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
    }
    var phone = "'" + String(d['Phone'] || '').slice(0, 20);   // leading ' keeps the number as text
    var row = [
      Utilities.formatDate(new Date(), 'Asia/Kolkata', 'dd MMM yyyy HH:mm'),
      clean(d['Child name']), clean(d['Parent name']), phone, clean(d['Age']),
      clean(d['Location']), clean(d['Batch']), 'New', ''
    ];
    sh.appendRow(row);
    if (NOTIFY_EMAIL) {
      MailApp.sendEmail(NOTIFY_EMAIL, 'New Chessopia registration: ' + row[1],
        HEADERS.slice(0, 7).map(function (h, i) { return h + ': ' + row[i]; }).join('\n'));
    }
    return out({ok: true});
  } catch (err) {
    return out({ok: false});
  } finally {
    lock.releaseLock();
  }
}

function clean(v) { return String(v == null ? '' : v).replace(/^[=+\-@]/, "'$&").slice(0, 200); }  // blocks formula injection
function out(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
