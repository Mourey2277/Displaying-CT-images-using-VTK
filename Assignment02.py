# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 14:09:28 2019

@author: Jannatul Mourey
"""

import vtk

# -------------------Loading data------------------
# Path of the dataset that contains the DICOM image sequence
ddir = r"CT" 

# Loading the dataset from the folder
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(ddir)
reader.Update()

# -------------------Volume Redering---------------------
# Creating an opacity function using different pixel value and opacity
opacityfunction = vtk.vtkPiecewiseFunction()
opacityfunction.AddPoint(-3024, 0)
opacityfunction.AddPoint(-77, 0)
opacityfunction.AddPoint(180, 0.2)
opacityfunction.AddPoint(260, 0.4)
opacityfunction.AddPoint(3071, 0.8)

# Creating a color transfer function using the provided values
colorfunction = vtk.vtkColorTransferFunction()
colorfunction.AddRGBPoint(-3024, 0, 0, 0)
colorfunction.AddRGBPoint(-77, 0.5, 0.2, 0.1)
colorfunction.AddRGBPoint(94, 0.9, 0.6, 0.3)
colorfunction.AddRGBPoint(179, 1, 0.9, 0.9)
colorfunction.AddRGBPoint(260, 0.6, 0, 0)
colorfunction.AddRGBPoint(3071, 0.8, 0.7, 1)

# Volume mapper for rendering DICOM with no shading
mapperVol = vtk.vtkSmartVolumeMapper()
mapperVol.SetInputConnection(reader.GetOutputPort())

# Adding color & opacity transfer functions while turning the shading off.
volumeprop1 = vtk.vtkVolumeProperty()
volumeprop1.SetScalarOpacity(opacityfunction)
volumeprop1.SetColor(colorfunction)
volumeprop1.ShadeOff()

# Creating actor for volume and set mapper and property
volume1 = vtk.vtkVolume()
volume1.SetMapper(mapperVol)
volume1.SetProperty(volumeprop1)

# Add volume to the respective renderer
ren1 = vtk.vtkRenderer()
ren1.AddVolume(volume1)
ren1.SetViewport(0, 0, 0.33, 1)#Setting the View Port
ren1.SetBackground(0.2, 0.2, 0.2)#Setting the background

# --------------------ISO Surface--------------------

# Apply Marching Cubes algorithm
iso = vtk.vtkMarchingCubes()
iso.SetInputConnection(reader.GetOutputPort())
iso.ComputeGradientsOn()
iso.ComputeScalarsOff()
iso.SetValue(0, 300)
    
# Polydata mapper for the iso-surface
mapperIso = vtk.vtkPolyDataMapper()
mapperIso.SetInputConnection(iso.GetOutputPort())
mapperIso.ScalarVisibilityOff()

# Actor for the iso surface
actorIso = vtk.vtkActor()
actorIso.SetMapper(mapperIso)
actorIso.GetProperty().SetColor(1.,1.,1.)

# ISO Rendering
ren2 = vtk.vtkRenderer()
ren2.SetViewport(.33, 0, .66, 1)#Setting the View Port
ren2.SetBackground(0.2, 0.2, 0.2)#Setting the background
ren2.AddActor(actorIso)

# ------------------ISO-Surface/ Volume Rendeing----------------------

# ISO and Volume Rendering 
ren3 = vtk.vtkRenderer()
ren3.SetViewport(0.66, 0, 1, 1)#Setting the View Port
ren3.SetBackground(0.2, 0.2, 0.2)#Setting the background
ren3.AddActor(actorIso)
ren3.AddVolume(volume1)

# ------------------Multiple Windows----------------------
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.AddRenderer(ren2)
renWin.AddRenderer(ren3)

renWin.Render()

#----------------Setting camera to the first render---------
# Set Camera 
ren1.GetActiveCamera().Zoom(2)
ren2.SetActiveCamera(ren1.GetActiveCamera())
ren3.SetActiveCamera(ren1.GetActiveCamera())
iren=vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

#---------------Getting the out as JPEG image-------

#Getting screenshot of the output window
windowToImageFilter = vtk.vtkWindowToImageFilter()
windowToImageFilter.SetInput(renWin)
windowToImageFilter.Update()
 
writer = vtk.vtkJPEGWriter()
writer.SetFileName("Output_of_Code.jpeg")

#writer.SetWriteToMemory(1)
writer.SetInputConnection(windowToImageFilter.GetOutputPort())
writer.Write()

iren.Initialize()# Initalizing the interactor for the loop 
iren.Start() # Start the event loop


