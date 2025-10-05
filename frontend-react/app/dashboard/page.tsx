export default function DashboardPage() {
  return (
    <div>
      <h2 className="text-2xl font-bold text-blue-600 mb-6">📈 لوحة التحكم</h2>

      <div className="grid grid-cols-3 gap-6">
        <div className="p-6 bg-white shadow rounded-2xl text-center">
          <h3 className="text-gray-500">إجمالي الفواتير</h3>
          <p className="text-2xl font-bold text-blue-600">0</p>
        </div>

        <div className="p-6 bg-white shadow rounded-2xl text-center">
          <h3 className="text-gray-500">إجمالي المبالغ</h3>
          <p className="text-2xl font-bold text-blue-600">0 ر.س</p>
        </div>

        <div className="p-6 bg-white shadow rounded-2xl text-center">
          <h3 className="text-gray-500">متوسط الفاتورة</h3>
          <p className="text-2xl font-bold text-blue-600">0 ر.س</p>
        </div>
      </div>

      <div className="bg-white mt-8 shadow rounded-2xl p-6 text-gray-500 text-center">
        📊 سيتم لاحقًا إضافة رسم بياني لعرض النشاط الأسبوعي للفواتير.
      </div>
    </div>
  );
}
