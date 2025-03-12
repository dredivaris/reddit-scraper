export default function Dashboard() {
  return (
    <div className="min-h-screen p-8">
      <div className="navbar bg-base-100 shadow-lg rounded-box mb-8">
        <div className="flex-1">
          <a className="btn btn-ghost normal-case text-xl">Dashboard</a>
        </div>
        <div className="flex-none">
          <button className="btn btn-ghost">Logout</button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Stats Cards */}
        <div className="stats shadow">
          <div className="stat">
            <div className="stat-title">Total Posts</div>
            <div className="stat-value">31K</div>
            <div className="stat-desc">Jan 1st - Feb 1st</div>
          </div>
        </div>

        <div className="stats shadow">
          <div className="stat">
            <div className="stat-title">New Users</div>
            <div className="stat-value">4,200</div>
            <div className="stat-desc">↗︎ 400 (22%)</div>
          </div>
        </div>

        <div className="stats shadow">
          <div className="stat">
            <div className="stat-title">Active Users</div>
            <div className="stat-value">1,200</div>
            <div className="stat-desc">↘︎ 90 (14%)</div>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <h2 className="card-title">Recent Activity</h2>
            <div className="overflow-x-auto">
              <table className="table w-full">
                <thead>
                  <tr>
                    <th>Type</th>
                    <th>Description</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Post</td>
                    <td>New content added</td>
                    <td>2 min ago</td>
                  </tr>
                  <tr>
                    <td>Comment</td>
                    <td>User feedback received</td>
                    <td>5 min ago</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <h2 className="card-title">Quick Actions</h2>
            <div className="flex flex-wrap gap-4">
              <button className="btn btn-primary">Create Post</button>
              <button className="btn btn-secondary">View Analytics</button>
              <button className="btn btn-accent">Settings</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 