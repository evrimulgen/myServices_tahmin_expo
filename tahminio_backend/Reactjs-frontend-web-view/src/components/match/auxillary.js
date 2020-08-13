import moment from 'moment';

function formatDate(unix) {
    var date = moment(unix * 1000);
    var formattedDate = date.format('DD/MM/YY');
    var formattedTime = date.format('HH:mm');

    return [formattedDate,formattedTime];
}

const _formatDate = formatDate;
export { _formatDate as formatDate };