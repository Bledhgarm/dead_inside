package com.example.figures;

import android.annotation.SuppressLint;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.DashPathEffect;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;

import androidx.annotation.Nullable;

public class MyView extends View {
    public MyView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
    }
    public MyView(Context context) {
        super(context);
    }
    int cellSize = 30;
    int width;
    int height;
    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        width = getWidth();
        height = getHeight();
        drawGrid(canvas);

    }
    public void drawGrid(Canvas canvas) {
        Paint paint = new Paint();

        for (int i = 0; i < width/cellSize; i++) {
            int x = i * cellSize;
            canvas.drawLine(x, 0, x, height, paint);
            paint.setColor(Color.parseColor("black"));
        }
        for (int i = 0; i < height/cellSize; i++) {
            int y = i * cellSize;
            canvas.drawLine(0, y, width, y, paint);
        }
    }

    @SuppressLint("ClickableViewAccessibility")
    @Override
    public boolean onTouchEvent(MotionEvent event) {
        if (event.getAction() == MotionEvent.ACTION_DOWN) {
            
            Log.i("onTouch", event.getAction() + "");
        }


        return true;
    }
}


