import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

// Shorten long period labels so they don't overlap on small screens
function shortLabel(label) {
  return label.length > 16 ? label.slice(0, 15) + '…' : label
}

function MetricsChart({ metrics }) {
  return (
    <section className="bg-white rounded-xl border border-slate-200 p-6">
      <h2 className="text-lg font-semibold text-slate-900">Financial Overview</h2>
      <p className="mt-1 text-sm text-slate-500">
        {metrics.metric_name} ({metrics.unit}), numbers taken directly from the evidence
      </p>
      
      <div className="mt-4 overflow-x-auto">       </div>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-200 text-left text-slate-500">
            <th className="py-2 font-medium">Period</th>
            <th className="py-2 text-right font-medium">{metrics.metric_name}</th>
          </tr>
        </thead>
        <tbody>
          {metrics.points.map((point, index) => (
            <tr key={index} className="border-b border-slate-100">
              <td className="py-2 text-slate-700">{point.period}</td>
              <td className="py-2 text-right font-medium text-slate-900">
                {point.value.toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="mt-6 h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={metrics.points}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="period" tick={{ fontSize: 11 }} tickFormatter={shortLabel} interval={0} />
            <YAxis tick={{ fontSize: 12 }} tickFormatter={(value) => value.toLocaleString()} />
            <Tooltip formatter={(value) => value.toLocaleString()} />
            <Bar dataKey="value" name={metrics.metric_name} fill="#2563eb" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}

export default MetricsChart