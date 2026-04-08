package com.tianluo.runtime.template

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val textView = TextView(this).apply {
            text = "Android Runtime Template\nV2 skeleton ready"
            textSize = 18f
            setPadding(40, 80, 40, 40)
        }

        setContentView(textView)
    }
}
