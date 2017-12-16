#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Analog Modulation VLC Link
# Author: Vicente Matus
# Description: Visible light communications (VLC) link under an analog modulation scheme. Intensity modulation (IM) over a modified LED and direct detection (DD) in a photodiode.
# Generated: Fri Dec 15 21:19:43 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx


class analog_mod_vlc_link(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Analog Modulation VLC Link")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.tx_gain = tx_gain = 0
        self.samp_rate = samp_rate = 1000000
        self.rx_gain = rx_gain = 10
        self.nbfm_max_dev = nbfm_max_dev = 44100
        self.center_freq = center_freq = 1000000
        self.audio_rate = audio_rate = 44100
        self.audio_interp = audio_interp = 4

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=-50,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(('addr=192.168.10.3', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(('addr=192.168.10.2', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=int(samp_rate),
                decimation=int(audio_interp*audio_rate),
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(audio_rate*audio_interp),
                decimation=int(samp_rate),
                taps=None,
                fractional_bw=None,
        )
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/vmatusic/Documents/VLC/gnuradio_codes/Loops/3449__patchen__trickyhop-abcd.wav', True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((0.75, ))
        self.audio_sink_0 = audio.sink(int(audio_rate), '', True)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=int(audio_rate),
        	quad_rate=int(audio_rate*audio_interp),
        	tau=75e-6,
        	max_dev=nbfm_max_dev,
        	fh=-1.0,
                )
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=int(audio_rate),
        	quad_rate=int(audio_rate*audio_interp),
        	tau=75e-6,
        	max_dev=nbfm_max_dev,
          )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.analog_nbfm_tx_0, 0), (self.rational_resampler_xxx_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.analog_nbfm_tx_0, 0))    
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.wxgui_fftsink2_0, 0))    

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)
        	

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)
        	

    def get_nbfm_max_dev(self):
        return self.nbfm_max_dev

    def set_nbfm_max_dev(self, nbfm_max_dev):
        self.nbfm_max_dev = nbfm_max_dev
        self.analog_nbfm_tx_0.set_max_deviation(self.nbfm_max_dev)
        self.analog_nbfm_rx_0.set_max_deviation(self.nbfm_max_dev)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_source_0.set_center_freq(self.center_freq, 0)
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate

    def get_audio_interp(self):
        return self.audio_interp

    def set_audio_interp(self, audio_interp):
        self.audio_interp = audio_interp


def main(top_block_cls=analog_mod_vlc_link, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
