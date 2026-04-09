package com.tianluo.runtime.template.runtime.app

import android.app.Service
import android.content.Intent
import android.os.IBinder

class RuntimeForegroundService : Service() {
    override fun onBind(intent: Intent?): IBinder? = null
}
