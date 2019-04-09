
/* getNextWeekDay: returns the dayOfWeek as date on the next week
    param: startDate(Date) - given startDate to consider nextWeek
    param: dayOfWeek(int) - the given day of the week to consider
                          - starts by 1 as monday to 7 as sunday
*/
function getNextWeekDay (startDate, dayOfWeek) {
  var currentDay = startDate.getDay() == 0 ? 7 : startDate.getDay();
  var dayOffset = dayOfWeek - currentDay + 7;

  startDate.setDate(startDate.getDate() + dayOffset);

  return startDate;
}

/* getNextWeek - called if button on search_ticket.html is pressed
                puts the start and enddate of the next week into
                the 2 deadline textboxes
*/
function getNextWeek() {
  //  Monday of the next week as date
  var nextMonday = getNextWeekDay(new Date(), 1);
  // Sunday of the next week as date
  var nextSunday = getNextWeekDay(new Date(), 7);

  document.getElementById("id_deadline_0").value = nextMonday.toLocaleDateString("de-DE");
  document.getElementById("id_deadline_1").value = nextSunday.toLocaleDateString("de-DE");

}
