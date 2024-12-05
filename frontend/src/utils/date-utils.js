import moment from 'moment-timezone';

export const formatDate = (dateString) => {
  const dayMap = {
    'Monday': 'Hai',
    'Tuesday': 'Ba',
    'Wednesday': 'Tư',
    'Thursday': 'Năm',
    'Friday': 'Sáu',
    'Saturday': 'Bảy',
    'Sunday': 'Chủ Nhật'
  };

  // Chuyển chuỗi ngày giờ thành đối tượng Moment với múi giờ GMT
  const date = moment.tz(dateString, 'GMT');

  // Lấy tên ngày trong tuần bằng tiếng Anh và chuyển sang tiếng Việt
  const dayOfWeek = dayMap[date.format('dddd')];

  // Định dạng ngày giờ theo yêu cầu
  const formattedDate = `Thứ ${dayOfWeek}, ${date.format('DD/MM/YYYY HH:mm')}`;

  return formattedDate;
};