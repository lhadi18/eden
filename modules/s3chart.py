import os
from io import StringIO
from gluon.storage import Storage
from gluon.html import IMG
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64

# Constants for easier management
CACHE_PATH = f"/{current.request.application}/static/cache/chart"
APPLICATIONS_PATH = "applications"
IMAGE_FORMAT = "image/png"

class S3Chart:
    """
        Module for graphing, currently a simple wrapper to matplotlib.
    """
    
    def __init__(self, path, width=9, height=6):
        self.filename = path
        self.width = width
        self.height = height
        self.fig = None

        try:
            self.fig = Figure(figsize=(width, height))
            self.canvas = FigureCanvas(self.fig)
        except ImportError:
            self.fig = None
            print("WARNING: S3Chart requires matplotlib for charting.")
    
    @staticmethod
    def get_cached_file(filename):
        """
            Return the content of the cached file, or None if not found.
        """
        cache_path = S3Chart._get_cached_path(filename)
        if cache_path and os.path.exists(cache_path):
            try:
                with open(cache_path, "r") as file:
                    return file.read()
            except Exception as e:
                print(f"Error reading cached file: {e}")
        return None
    
    @staticmethod
    def _get_cached_path(filename):
        """
            Return the full path to the cached file.
        """
        return f"{APPLICATIONS_PATH}{CACHE_PATH}/{filename}.png"
    
    @staticmethod
    def store_cached_file(filename, image):
        """
            Save image to cache and return the relative path.
        """
        cache_path = S3Chart._get_cached_path(filename)
        try:
            with open(cache_path, "wb") as f:
                f.write(image)
            return cache_path
        except Exception as e:
            print(f"Error storing cached file: {e}")
        return None
    
    @staticmethod
    def purge_cache(prefix=None):
        """
            Delete cached files with optional filename prefix.
        """
        folder = f"{APPLICATIONS_PATH}{CACHE_PATH}/"
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if prefix is None or file.startswith(prefix):
                    os.remove(os.path.join(folder, file))
    
    def draw(self, output="xml"):
        """
            Render the chart and return an image embedded in an IMG tag (XML).
        """
        if not self.fig:
            return "Matplotlib not installed"

        chart = Storage(body=StringIO(), headers=Storage())
        chart.headers["Content-Type"] = IMAGE_FORMAT

        self.canvas.print_figure(chart.body)
        image = chart.body.getvalue()
        cache_path = self.store_cached_file(self.filename, image)
        
        if output == "xml":
            if cache_path:
                return IMG(_src=cache_path)
            else:
                base64_img = base64.b64encode(image).decode("utf-8")
                return IMG(_src=f"data:{IMAGE_FORMAT};base64,{base64_img}")
        else:
            current.response.headers["Content-Type"] = IMAGE_FORMAT
            return image
    
    def survey_hist(self, title, data, bins, min_val, max_val, xlabel=None, ylabel=None):
        """
            Draw a Histogram.
        """
        if not self.fig:
            return "Matplotlib not installed"
        
        from numpy import arange

        ax = self.fig.add_subplot(111)
        ax.hist(data, bins=bins, range=(min_val, max_val))

        label = arange(0, bins + 1) * (max_val / bins)
        ax.set_xticks(label)
        ax.set_xticklabels(label, rotation=30)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

    # -------------------------------------------------------------------------
    def survey_pie(self, title, data, label):
        """
            Draw a Pie Chart
                - used by the Survey module
        """

        fig = self.fig
        if not fig:
            return "Matplotlib not installed"

        # Draw a pie chart
        ax = fig.add_subplot(111)
        ax.pie(data, labels=label)
        ax.legend()
        ax.set_title(title)

    # -------------------------------------------------------------------------
    def survey_bar(self, title, data, labels, legendLabels):
        """
            Draw a Bar Chart
                - used by the Survey module
        """

        barColourList = ["#F2D7A0", "#7B77A8", "#69889A", "#9D7B34"]
        barColourListExt = [(242, 215, 160),
                            (123, 118, 168),
                            (105, 136, 154),
                            (157, 123, 52)
                           ]
        fig = self.fig
        if not fig:
            return "Matplotlib not installed"

        from numpy import arange

        # Draw a bar chart
        if not isinstance(data[0],list):
            dataList = [data]
        else:
            dataList = data
        legendColCnt = 3
        cnt = len(labels)
        dcnt = len(dataList)
        lcnt = 0
        if legendLabels != None:
            lcnt = (len(legendLabels) + legendColCnt - 1) / legendColCnt
        width = 0.9 / dcnt
        offset = 0
        gap = 0.1 / dcnt
        bcnt = 0
        bars = []
        height = max(0.2, 0.85 - (0.04 * lcnt))
        rect = [0.08, 0.08, 0.9, height]
        ax = fig.add_axes(rect)
        for data in dataList:
            left = arange(offset, cnt + offset)    # the x locations for the bars
            if bcnt < 3:
                colour = barColourList[bcnt]
            else:
                colour = []
                colourpart = barColourListExt[bcnt%4]
                divisor = 256.0 - (32 * bcnt/4)
                if divisor < 0.0:
                    divisor = divisor * -1
                for part in colourpart:
                    calc = part/divisor
                    while calc > 1.0:
                        calc -= 1
                    colour.append(calc)
            plot = ax.bar(left, data, width=width, color=colour)
            bars.append(plot[0])
            bcnt += 1
            offset += width + gap
        left = arange(cnt)
        lblAdjust = (1.0 - gap) * 0.5
        if cnt <= 3:
            angle = 0
        elif cnt <= 10:
            angle = -10
        elif cnt <= 20:
            angle = -30
        else:
            angle = -45
        ax.set_xticks(left + lblAdjust)
        try: # This function is only available with version 1.1 of matplotlib
            ax.set_xticklabels(labels, rotation=angle)
            ax.tick_params(labelsize=self.width)
        except AttributeError:
            newlabels = []
            for label in labels:
                if len(label) > 12:
                    label = label[0:10] + "..."
                newlabels.append(label)
            ax.set_xticklabels(newlabels)
        ax.set_title(title)
        if legendLabels != None:
            fig.legend(bars,
                       legendLabels,
                       "upper left",
                       mode="expand",
                       ncol = legendColCnt,
                       prop={"size":10},
                      )

# END =========================================================================
