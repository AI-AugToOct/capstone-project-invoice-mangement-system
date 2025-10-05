export default function Home() {
  return (
    <div className="text-center space-y-10">
      <section className="bg-white rounded-2xl shadow-md p-10 max-w-2xl mx-auto border border-gray-100">
        <h2 className="text-3xl font-bold text-green-700 mb-3">مرحبًا بك في مفوتر 👋</h2>
        <p className="text-gray-600 text-lg">
          نظام إدارة الفواتير وتحليلها باستخدام الذكاء الاصطناعي لتوفير وقتك وجهدك.
        </p>
      </section>

      <section className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        <div className="bg-green-100 text-green-800 rounded-xl p-6 shadow">
          <h3 className="text-lg font-bold mb-2">📄 إجمالي الفواتير</h3>
          <p className="text-2xl font-semibold">0</p>
        </div>

        <div className="bg-green-200 text-green-900 rounded-xl p-6 shadow">
          <h3 className="text-lg font-bold mb-2">💰 إجمالي المبالغ</h3>
          <p className="text-2xl font-semibold">0 ر.س</p>
        </div>

        <div className="bg-green-100 text-green-800 rounded-xl p-6 shadow">
          <h3 className="text-lg font-bold mb-2">📊 متوسط الفاتورة</h3>
          <p className="text-2xl font-semibold">0 ر.س</p>
        </div>
      </section>

      <section className="text-gray-500 text-md">
        📈 سيتم لاحقًا إضافة رسم بياني لعرض النشاط الأسبوعي للفواتير.
      </section>
    </div>
  );
}
