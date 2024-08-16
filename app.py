import streamlit as st

# Spline code snippet with a centered button
spline_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            overflow: hidden;
        }
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            position: relative;
        }
        .button {
            position: absolute;
            z-index: 10;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .button:hover {
            background-color: #0056b3;
        }
    </style>
    <script type="module" src="https://unpkg.com/@splinetool/viewer@1.9.13/build/spline-viewer.js"></script>
</head>
<body>
    <div class="container">
        <spline-viewer url="https://prod.spline.design/yQ3ZGU0S5gjhg9m6/scene.splinecode"></spline-viewer>
        <button class="button">Click Me</button>
    </div>
</body>
</html>
"""

# Display Spline with centered button in Streamlit
st.components.v1.html(spline_code, height=600, scrolling=True)
